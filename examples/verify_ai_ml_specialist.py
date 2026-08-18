import uuid

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

from deepagents.backends.filesystem import FilesystemBackend
from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace
from system_design_planner.permissions import DESIGN_SESSION_PERMISSIONS
from system_design_planner.runtime import run_with_hitl
from system_design_planner.subagents import build_ai_ml_specialist

load_dotenv()

backend = FilesystemBackend(root_dir=".")
checkpointer = MemorySaver()

agent = build_planner_agent(
    backend=backend,
    permissions=DESIGN_SESSION_PERMISSIONS,
    checkpointer=checkpointer,
    memory=["/memory/AGENTS.md"],
    subagents=[build_ai_ml_specialist(backend)],
)

config = {"configurable": {"thread_id": str(uuid.uuid4())}}

result = run_with_hitl(
    agent,
    config,
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Delegate to your ai-ml-specialist: what's the right way "
                    "to serve and access LLMs for our agentic workflows, "
                    "given our current scoping constraints?"
                ),
            }
        ]
    },
)

print(get_final_text(result))
print_message_trace(result)
