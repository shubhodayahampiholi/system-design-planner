import asyncio

from databricks.sdk import WorkspaceClient
from databricks_langchain import DatabricksMCPServer, DatabricksMultiServerMCPClient

CATALOG = "knowledge_platform"
SCHEMA = "default"


async def _fetch_uc_function_tools():
    workspace_client = WorkspaceClient()
    host = workspace_client.config.host
    mcp_client = DatabricksMultiServerMCPClient([
        DatabricksMCPServer(
            name="uc-functions",
            url=f"{host}/api/2.0/mcp/functions/{CATALOG}/{SCHEMA}",
            workspace_client=workspace_client,
        ),
    ])
    return await mcp_client.get_tools()


def get_databricks_uc_function_tools():
    """Synchronously fetch MCP tools for Unity Catalog Functions.

    MCP tool discovery is async (await mcp_client.get_tools()), but the rest
    of this project uses synchronous .invoke() throughout. The async fetch
    happens once, here, at setup time - the agent itself never needs to run
    async, only this one-time discovery step does.
    """
    return asyncio.run(_fetch_uc_function_tools())
