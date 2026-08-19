def get_final_text(result) -> str:
    """Extract just the visible text from the final message.

    With extended thinking enabled, an AIMessage's content can be a list of
    typed blocks (thinking, text, ...) rather than a plain string. This pulls
    out only the text blocks - thinking blocks carry a cryptographic signature
    for multi-turn verification, not something meant for display.
    """
    content = result["messages"][-1].content
    if isinstance(content, str):
        return content
    return "\n".join(
        block["text"] for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    )


def print_message_trace(result):
    """Print each message in an invoke() result with any tool calls made."""
    for i, msg in enumerate(result["messages"]):
        tool_calls = getattr(msg, "tool_calls", None)
        label = type(msg).__name__
        if tool_calls:
            label += f" -> calls: {[tc['name'] for tc in tool_calls]}"
        content = getattr(msg, "content", None)
        if isinstance(content, list) and any(
            isinstance(b, dict) and b.get("type") == "thinking" for b in content
        ):
            label += " [extended thinking present]"
        print(f"[{i}] {label}")


def print_thinking(result):
    """Print thinking content, and explicitly report when it's empty.

    Distinguishes 'no thinking block exists' from 'a thinking block exists
    but its text is empty' - the two look identical if you only check
    truthiness, and we need to know which one we're actually seeing.
    """
    for i, msg in enumerate(result["messages"]):
        content = getattr(msg, "content", None)
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "thinking":
                text = block.get("thinking", "")
                has_sig = bool(block.get("signature"))
                if text:
                    print(f"[{i}] THINKING: {text}\n")
                else:
                    print(f"[{i}] THINKING BLOCK PRESENT BUT EMPTY (signature present: {has_sig})\n")

def print_delegation_targets(result):
    """Print which subagent each 'task' tool call actually targeted.

    print_message_trace only shows the tool name ('task'), never which
    specialist it was routed to - we've been inferring that from context
    every time rather than confirming it directly from the trace.
    """
    for i, msg in enumerate(result["messages"]):
        tool_calls = getattr(msg, "tool_calls", None) or []
        for tc in tool_calls:
            if tc["name"] == "task":
                target = tc["args"].get("subagent_type", "?")
                print(f"[{i}] task -> {target}")


def classify_tool_call(tool_call, mcp_tool_names):
    """Categorize a tool call for display: subagent, MCP, skill, filesystem, or plain tool.

    Reuses the same signals proven out earlier in this build:
    - 'task' calls with subagent_type = delegation (print_delegation_targets)
    - a name matching a known MCP tool = a managed MCP hit
    - a read_file targeting /skills/project/.../SKILL.md = a skill load
      (confirmed via LangSmith this is how progressive disclosure surfaces)
    - everything else filesystem-shaped = plain filesystem ops
    """
    name = tool_call["name"]
    args = tool_call.get("args", {})

    if name == "task":
        return "subagent", args.get("subagent_type", "?")
    if name in mcp_tool_names:
        return "mcp", name
    if name == "read_file":
        path = str(args.get("file_path", ""))
        if "/skills/project/" in path and path.endswith("SKILL.md"):
            skill_name = path.split("/")[-2]
            return "skill", skill_name
    if name in ("read_file", "write_file", "edit_file", "ls", "glob", "grep", "delete"):
        return "filesystem", name
    return "tool", name
