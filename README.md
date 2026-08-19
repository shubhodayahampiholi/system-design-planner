# system-design-planner

A hands-on reference build of [LangChain's DeepAgents](https://github.com/langchain-ai/deepagents)
harness, used to work through what the harness actually does under real load —
not what its docs claim it does. Every mechanism in this repo — filesystem
backends, permissions, subagent delegation, memory, human-in-the-loop, skills,
MCP — was verified against actual source code, real LangSmith traces, or real
runs, not assumed from documentation.

The vehicle is a genuine use case: an AI-architecture planning assistant for
an Azure + Databricks estate, deliberately chosen because "use native
tooling" is a real, currently unresolved ambiguity between the Databricks-
native and Azure-native (Microsoft Foundry) stacks — exactly the kind of
long-horizon, multi-step problem a harness like this exists to help with.

## What's actually in here

- **Two filesystem backends** — in-memory (`StateBackend`) and real-disk
  (`FilesystemBackend`), with path-scoped eny`/`interrupt`
  permission rules
- **Five subagents** — four domain specialists (governance, AI/ML,
  orchestration, network) plus a generic extraction subagent, including
  genuine **cross-provider delegation**: the planner runs on Claude, one
  subagent runs on OpenAI, confirmed via a real LangSmithrace
- **Real human-in-the-loop** — interrupt-gated writes to persistent memory,
  with actual approve/reject decisions (includina rejection reason sent
  back to the model), working in both the terminal and the Streamlit UI
- **Persistent, agent-maintained memory** (`memory/AGENTS.md`) — the agent
  writes to it, but every write pauses for human approval first
- **ree real Skills** (`skills/project/`) — progressive disclosure confirmed via LangSmith (`SKILL.md` genuinely read on demand, not just
  present in context), covering scoping judgment, RAG/embedding design, and
  data pipeline validation
- **A real custom tool** — Tavily-backed live web search, used to check
  whether something in the static reference corpus has gone stale
- **A real MCP integration** — Databricks' managed Unity Catalog Function
  MCP server, discovered and called live, not mocked
- **A Streamlit UI** (`app.py`) — chat interface with a live trace panel
  showing tool calls, subagent delegation, and MCP hits as they happen, plus
  in-UI HITL approve/reject

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- API keys: Anthropic, OpenAI, Tavily (LangSmith optional but recommended)
- A Daks workspace with a Unity Catalog function, for the MCP example
  and the full Streamlit app specifically — everything else runs fully local

## Setup

```bash
uv sync
cp .env.example .env   # then fill in your real keys
```

## Project structure
system-design-planner/
├── app.py # Streamlit UI
├── knowledge_base/ # grounded, dated reference corpus
├── skills/project/ # three SKILL.md files
├── memory/AGENTS.md # agent-maintained, HITL-gated memory
├── examples/ # ordered, runnable walkthroughs
└── src/system_design_planner/
├── agent.py # build_planner_agent() factory
├── streamlit_agent.py # full-agent builder for the UI
├── prompts.py
├── permissions.py
├── subagents.py
├── tools.py # Tavily
├── mcp_tools.py # Databricks MCP
├── runtime.py # run_with_hitl (terminal HITL loop)
└── debug.py # trace/thinking/classification helpers


## Learning path

Read and run these in order. Each one proves one mechanism in isolation
before the next builds on it.

1. `examples/verify_harness_runs.py` — bare harness, confirms the agent
   genuinely calls its filesystem tools rather than guessing plausibly
2. `examples/planner_persona.py` — confirms a custom `system_prompscoped to a reference corpus
4. `examples/verify_extractor_subagent.py` — first subagent, on a different
   model than the parent
5. `examples/verify_hitl_memory_gate.py` — real interrupt/resume, real human
   approval, not a hardcoded self-approval
6. `examples/verify_governancecialist.py`,
   `verify_ai_ml_specialist.py`, `verify_orchestration_specialist.py`,
   `verify_network_specialist.py` — each domain specialist individually
7. `examples/verify_multi_specialist_routing.py` — the parent choosing
   delegation on its own, including real parallel fan-out
8. `examples/verify_web_search_tool.py` — a custom Tavily-backed tool
9. `examples/verify_skill_loading.py`, `verify_technical_skills.py` — Skills,
   mechanism then content relevance
10. `examples/verify_databricks_mcp.py` — a real Databricks managed MCP
    server, discovered and called live
11. `app.py` — everything above, in one Streamlun streamlit run app.py`

## Known limitations, found while building this

Documented because they're genuinely useful to know, not because they're
flattering:

- **The model confabulates under a bare rejection.** Told "no" with no
  reason, it invents a plausible-sounding one and retries — observed
  independently in both the terminal and Streamlit builds. Always pass a
  real `message` on a `RejectDecision`.
- **`claude-sonnet-5` gets zero harness-profile tuning, silently.**
  DeepAgents' built-in prompt profiles are pinned to specific model
  generatns (Sonnet 4.6, not 5) with no provider-wide fallback — and no
  warning when nothing matches.
- **Skill loading inside a subagent isn't visible in a default Streamlit
  trace.** Confirmed working via LangSmith; not surfaced live without
  `subgraphs=True` on `.astream()`, which changes thetream's chunk shape
  and wasn't applied here.
- **A real, upstream `SummarizationMiddleware` + extended-thinking bug**
  (tracked at `langchain-ai/langchain#34794`) surfaced once a session ran
  long enough to trigger automatic summarization.

## License

MIT
