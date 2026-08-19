from langgraph.checkpoint.memory import MemorySaver

from deepagents.backends.filesystem import FilesystemBackend
from system_design_planner.agent import build_planner_agent
from system_design_planner.mcp_tools import get_databricks_uc_function_tools
from system_design_planner.permissions import DESIGN_SESSION_PERMISSIONS
from system_design_planner.subagents import (
    build_ai_ml_specialist,
    build_governance_specialist,
    build_network_specialist,
    build_orchestration_specialist,
)
from system_design_planner.tools import check_current_standards


def build_full_agent():
    """Build the complete planner: all four specialists, all three skills,
    Tavily, MCP, memory, permissions, checkpointer - everything proven
    individually across this build, wired together for real use.

    MCP tool discovery happens once here, synchronously (get_databricks_uc_function_tools
    manages its own event loop internally), before any per-turn async
    streaming starts - avoids nesting asyncio.run() calls.
    """
    backend = FilesystemBackend(root_dir=".")
    checkpointer = MemorySaver()

    mcp_tools = get_databricks_uc_function_tools()

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
        tools=[check_current_standards, *mcp_tools],
    )
    return agent, mcp_tools
