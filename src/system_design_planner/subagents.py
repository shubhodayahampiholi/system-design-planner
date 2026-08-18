from deepagents import SubAgent

REFERENCE_EXTRACTOR: SubAgent = {
    "name": "reference-extractor",
    "description": (
        "Extracts structured, factual capabilities from the knowledge_base "
        "reference files for a specific platform or topic. Delegate here "
        "before proposing any subsystem design, so decisions are grounded "
        "in verified platform facts rather than assumption. Do not use this "
        "subagent for design reasoning or tradeoffs - extraction only."
    ),
    "system_prompt": (
        "You are a fact-extraction specialist. Given a topic, find the "
        "relevant file(s) in your working directory, read them, and return "
        "ONLY a bullet list of the concrete facts relevant to that topic - "
        "no narrative, no design opinions, no recommendations. If a fact is "
        "explicitly flagged as an open question or unverified in the source "
        "file, preserve that flag in your output rather than smoothing it "
        "over into a confident-sounding statement."
    ),
    "model": "openai:gpt-5.6-luna",
}


def build_governance_specialist(backend) -> SubAgent:
    """Construct the governance-specialist subagent.

    Needs its own MemoryMiddleware instance because subagents don't
    automatically inherit the parent's memory - confirmed directly from the
    SubAgent TypedDict source, which has no `memory` field at all. Without
    this, the subagent would have no way to know about scoping decisions
    already recorded in /memory/AGENTS.md.
    """
    from deepagents.middleware.memory import MemoryMiddleware

    return {
        "name": "governance-specialist",
        "description": (
            "Reasons about Unity Catalog governance, lineage, and the "
            "Databricks-Microsoft Foundry governance boundary for this "
            "architecture. Delegate here for questions about access control, "
            "data lineage, or governance scope - not AI/ML serving, "
            "orchestration, or networking."
        ),
        "system_prompt": (
            "You are a governance specialist for an Azure + Databricks AI "
            "architecture. Before answering, check /memory/AGENTS.md for any "
            "recorded scoping decisions - they are binding constraints on "
            "your recommendation, not suggestions. Read "
            "/knowledge_base/unity_catalog_governance.md and "
            "/knowledge_base/microsoft_foundry_connector.md before proposing "
            "anything. Flag any open questions from those files rather than "
            "resolving them yourself."
        ),
        "middleware": [MemoryMiddleware(backend=backend, sources=["/memory/AGENTS.md"])],
        "skills": ["/skills/project/"],
    }


def build_ai_ml_specialist(backend) -> SubAgent:
    """Construct the ai-ml-specialist subagent.

    Same MemoryMiddleware pattern as governance-specialist - confirmed once,
    applies identically to every domain specialist we build from here on.
    """
    from deepagents.middleware.memory import MemoryMiddleware

    return {
        "name": "ai-ml-specialist",
        "description": (
            "Reasons about the AI/ML serving layer - model hosting, vector "
            "search, agent frameworks - for this architecture. Delegate here "
            "for questions about model serving, LLM access paths, vector "
            "search, or agent runtime choices - not governance, "
            "orchestration, or networking."
        ),
        "system_prompt": (
            "You are an AI/ML platform specialist for an Azure + Databricks "
            "architecture. Before answering, check /memory/AGENTS.md for any "
            "recorded scoping decisions - they are binding constraints on "
            "your recommendation, not suggestions. Read "
            "/knowledge_base/mosaic_ai_platform.md and "
            "/knowledge_base/microsoft_foundry_connector.md before proposing "
            "anything. This is exactly where the native-tooling ambiguity "
            "bites hardest - Databricks Mosaic AI vs. Microsoft Foundry's "
            "model/agent stack - so be explicit about which side of that "
            "line each recommendation falls on. Flag open questions from "
            "those files rather than resolving them yourself."
        ),
        "middleware": [MemoryMiddleware(backend=backend, sources=["/memory/AGENTS.md"])],
    }


def build_orchestration_specialist(backend) -> SubAgent:
    """Construct the orchestration-specialist subagent.

    Domain is deliberately distinct from ai-ml-specialist: that one decides
    WHICH model/vector-search/agent-framework tools get used, this one
    decides WHERE the agent runtime process itself actually executes.
    Real overlap exists (Agent Bricks appears in both knowledge_base files)
    - the system prompt below is explicit about the boundary so delegation
    routes correctly.
    """
    from deepagents.middleware.memory import MemoryMiddleware

    return {
        "name": "orchestration-specialist",
        "description": (
            "Reasons about where the agent runtime/compute itself lives - "
            "Databricks Apps vs. Azure-side hosting (Foundry Agent Service, "
            "Container Apps, Functions). Delegate here for hosting/compute "
            "boundary questions - not which model or vector search tool to "
            "use (that's ai-ml-specialist), and not governance or networking."
        ),
        "system_prompt": (
            "You are an orchestration/runtime-hosting specialist for an "
            "Azure + Databricks AI architecture. Before answering, check "
            "/memory/AGENTS.md for recorded scoping decisions - binding "
            "constraints, not suggestions. Read "
            "/knowledge_base/orchestration_runtime.md and "
            "/knowledge_base/microsoft_foundry_connector.md before "
            "proposing anything. Your focus is specifically WHERE the "
            "agent process runs and what compute boundary that implies - "
            "not which model or tool the agent calls once running. Flag "
            "open questions from those files rather than resolving them "
            "yourself, and be explicit about anything marked unconfirmed "
            "in the source material."
        ),
        "middleware": [MemoryMiddleware(backend=backend, sources=["/memory/AGENTS.md"])],
    }


def build_network_specialist(backend) -> SubAgent:
    """Construct the network-specialist subagent - the last of the four."""
    from deepagents.middleware.memory import MemoryMiddleware

    return {
        "name": "network-specialist",
        "description": (
            "Reasons about identity and network topology - VNet injection, "
            "Private Link, serverless connectivity, Entra ID - for this "
            "architecture. Delegate here for network/identity boundary "
            "questions - not governance, model serving, or runtime hosting."
        ),
        "system_prompt": (
            "You are an identity and networking specialist for an Azure + "
            "Databricks AI architecture. Before answering, check "
            "/memory/AGENTS.md for recorded scoping decisions - binding "
            "constraints, not suggestions. Read "
            "/knowledge_base/identity_networking.md before proposing "
            "anything. Pay particular attention to the serverless + VNet "
            "connectivity section - this is a common source of real "
            "architectural mistakes if glossed over. Flag open questions "
            "rather than resolving them yourself."
        ),
        "middleware": [MemoryMiddleware(backend=backend, sources=["/memory/AGENTS.md"])],
    }
