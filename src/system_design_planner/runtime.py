from langgraph.types import Command


def run_with_hitl(agent, config, initial_input, *, max_rounds: int = 3):
    """Invoke an agent and interactively resolve any interrupts that fire.

    Any subagent can legitimately decide to write to /memory/AGENTS.md,
    which is gated - not just the dedicated HITL example. Every script that
    invokes this agent needs to handle a possible pause, or it silently
    leaves the graph paused and exits, as verify_network_specialist.py just
    did. Centralised here so that behaviour is consistent everywhere rather
    than re-implemented per script.
    """
    result = agent.invoke(initial_input, config=config)

    round_num = 1
    while True:
        state = agent.get_state(config)
        if not state.interrupts:
            break
        if round_num > max_rounds:
            print(f"\n--- STOPPING: {max_rounds} rounds without resolution. ---")
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

        result = agent.invoke(Command(resume={"decisions": [decision]}), config=config)
        round_num += 1

    return result
