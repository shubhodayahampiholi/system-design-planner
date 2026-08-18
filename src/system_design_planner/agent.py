from deepagents import create_deep_agent

from system_design_planner.prompts import PLANNER_SYSTEM_PROMPT

MODEL = "claude-sonnet-5"


def build_planner_agent(*, system_prompt: str | None = PLANNER_SYSTEM_PROMPT, **kwargs):
    """Construct the system-design-planner deep agent.

    Centralised so every example and future subagent/skill/memory wiring
    shares one definition of the model and base config, rather than each
    example re-declaring create_deep_agent(...) independently.

    Pass system_prompt=None to get the bare, unconfigured harness — used by
    verify_harness_runs.py, which is deliberately testing the harness itself,
    not the persona.
    """
    return create_deep_agent(model=MODEL, system_prompt=system_prompt, **kwargs)
