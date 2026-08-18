import uuid

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

from deepagents.backends.filesystem import FilesystemBackend
from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace
from system_design_planner.permissions import DESIGN_SESSION_PERMISSIONS
from system_design_planner.runtime import run_with_hitl
from system_design_planner.subagents import (
    build_ai_ml_specialist,
    build_governance_specialist,
    build_network_specialist,
    build_orchestration_specialist,
)

load_dotenv()

backend = FilesystemBackend(root_dir=".")
checkpointer = MemorySaver()

agent = build_planner_agent(
    backend=backend,
    permissions=DESIGN_SESSION_PERMISSIONS,
    checkpointer=checkpointer,
    memory=["/memory/AGENTS.md"],
    subagents=[
        build_governance_specialist(backend),
        build_ai_ml_specialist(backend),
        build_orchestration_specialist(backend),
        build_network_specialist(backend),
    ],
)

config = {"configurable": {"thread_id": str(uuid.uuid4())}}

# Deliberately NOT naming which specialist(s) to use 
result = run_with_hitl(
    agent,
    config,
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "We want an internal agentic assistant that lets "
                    "analysts query governed customer data via RAG, hosted "
                    "reliably, and able to reach a private database in our "
                    "VNet for supplementary lookups. Give me a consolidated "
                    "recommendation, using whichever specialists are "
                    "actually relevant."
                ),
            }
        ]
    },
)

print(get_final_text(result))
print_message_trace(result)

print("\n\n=== FOLLOW-UP TURN: answering the scoping questions ===\n")

result = run_with_hitl(
    agent,
    config,  # same thread_id - this is a continuation, not a new conversation
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Answers: 1) Keep compute serverless, reach the DB via "
                    "Private Link/NCC rather than VNet injection. 2) "
                    "Enterprise-wide, moderate volume - prefer provisioned "
                    "throughput over pure pay-per-token, no hard SLA number "
                    "yet. 3) Read-only supplementary lookup via a tool call "
                    "at query time, not part of the RAG index itself. 4) "
                    "Yes, the governed customer data is already in Unity "
                    "Catalog as Delta tables, ready for RAG. Please proceed "
                    "and delegate to whichever specialists are relevant."
                ),
            }
        ]
    },
)

print(get_final_text(result))
print_message_trace(result)
from system_design_planner.debug import print_delegation_targets
print_delegation_targets(result)
