from dotenv import load_dotenv

from system_design_planner.agent import build_planner_agent
from system_design_planner.debug import get_final_text, print_message_trace
from system_design_planner.mcp_tools import get_databricks_uc_function_tools

load_dotenv()

print(">>> Fetching tools from the Databricks managed MCP server...")
mcp_tools = get_databricks_uc_function_tools()
print(f">>> Discovered {len(mcp_tools)} tool(s): {[t.name for t in mcp_tools]}")

agent = build_planner_agent(tools=mcp_tools)


async def main():
    result = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": "Call the mcp_verification_check function and report exactly what it returns.",
            }
        ]
    })
    print(get_final_text(result))
    print_message_trace(result)


import asyncio
asyncio.run(main())
