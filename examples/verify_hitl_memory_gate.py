import uuid

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from deepagents.backends.filesystem import FilesystemBackend
from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace, print_thinking
from system_design_planner.permissions import DESIGN_SESSION_PERMISSIONS

load_dotenv()

MAX_ROUNDS = 3  # circuit breaker - stop asking the human to referee forever

backend = FilesystemBackend(root_dir=".")
checkpointer = MemorySaver()

agent = build_planner_agent(
    backend=backend,
    permissions=DESIGN_SESSION_PERMISSIONS,
    checkpointer=checkpointer,
    memory=["/memory/AGENTS.md"],
)

thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

print(">>> LLM call: asking the agent to save a scoping decision to memory...")
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "For this design: 'native tooling' means the Databricks-native "
                    "stack only - do not consider Azure AI Foundry / Microsoft "
                    "Foundry in scope. Please save this scoping decision to memory "
                    "now, before we go any further."
                ),
            }
        ]
    },
    config=config,
)
print_thinking(result)

round_num = 1
while True:
    state = agent.get_state(config)
    if not state.interrupts:
        break

    if round_num > MAX_ROUNDS:
        print(f"\n--- STOPPING: {MAX_ROUNDS} rounds of interrupts without resolution. ---")
        print("The agent isn't converging - this needs a different instruction from")
        print("the human, not another round of approve/reject on the same request.")
        break

    action = state.interrupts[0].value["action_requests"][0]
    print(f"\n--- PAUSED (round {round_num}). Requested tool call: ---")
    print(f"  tool: {action['name']}")
    print(f"  args: {action['args']}")

    answer = input("\nApprove this write? [y/n]: ").strip().lower()
    if answer == "y":
        decision = {"type": "approve"}
    else:
        reason = input("Reason for rejecting (sent to the model): ").strip()
        decision = {"type": "reject", "message": reason or "Rejected by the human reviewer."}

    print(f"\n>>> Resuming (round {round_num}) with your decision...")
    result = agent.invoke(Command(resume={"decisions": [decision]}), config=config)
    print_thinking(result)
    round_num += 1

print("\n--- Final response ---")
print(get_final_text(result))
print_message_trace(result)
