from langchain_core.tools import tool
from langchain_tavily import TavilySearch

_tavily_instance = None


def _get_tavily() -> TavilySearch:
    """Lazily construct the Tavily client on first real use, not at import.

    TavilySearch reads TAVILY_API_KEY at construction time. Building it at
    module level meant it ran the instant this file was imported - before
    load_dotenv() had necessarily run in whatever script imported it. This
    defers construction until the tool is actually called, by which point
    .env is guaranteed loaded.
    """
    global _tavily_instance
    if _tavily_instance is None:
        _tavily_instance = TavilySearch(max_results=3, topic="general")
    return _tavily_instance


@tool
def check_current_standards(query: str) -> str:
    """Search the live web to verify whether a platform capability, naming,
    or integration detail is still current.

    Use this specifically to check something already pulled from
    knowledge_base against what's true right now - not for open-ended
    research. The knowledge_base files are static reference material that
    can go stale; this tool exists to catch that.

    Args:
        query: A specific, narrow question about current state - e.g.
            "is Microsoft Foundry still called that" - not a broad topic.
    """
    result = _get_tavily().invoke({"query": query})
    return str(result)
