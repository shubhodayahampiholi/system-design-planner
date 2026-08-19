import asyncio
import uuid

import streamlit as st
from dotenv import load_dotenv
from langgraph.types import Command

from system_design_planner.debug import classify_tool_call
from system_design_planner.streamlit_agent import build_full_agent

load_dotenv()

st.set_page_config(page_title="System Design Planner", page_icon=":building_construction:")
st.title(":building_construction: System Design Planner")

ICONS = {"subagent": ":handshake:", "mcp": ":electric_plug:", "skill": ":jigsaw:", "filesystem": ":file_folder:", "tool": ":wrench:"}

if "agent" not in st.session_state:
    with st.spinner("Setting up agent - fetching MCP tools, wiring specialists..."):
        agent, mcp_tools = build_full_agent()
    st.session_state.agent = agent
    st.session_state.mcp_tool_names = {t.name for t in mcp_tools}
    st.session_state.config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    st.session_state.history = []
    st.session_state.trace_log = []
    st.session_state.seen_count = 0
    st.session_state.pending_interrupt = None

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

trace_expander = st.expander(":mag: Execution trace", expanded=True)
with trace_expander:
    for line in st.session_state.trace_log:
        st.markdown(line)


def render_new_messages(messages):
    new = messages[st.session_state.seen_count:]
    for msg in new:
        for tc in (getattr(msg, "tool_calls", None) or []):
            category, label = classify_tool_call(tc, st.session_state.mcp_tool_names)
            line = f"{ICONS.get(category, ':wrench:')} **{category}** -> `{label}`"
            st.session_state.trace_log.append(line)
            with trace_expander:
                st.markdown(line)
    st.session_state.seen_count = len(messages)


def run_turn(initial_input):
    async def _run():
        async for chunk in st.session_state.agent.astream(
            initial_input, config=st.session_state.config, stream_mode="values"
        ):
            render_new_messages(chunk.get("messages", []))
        return await st.session_state.agent.aget_state(st.session_state.config)

    state = asyncio.run(_run())

    if state.interrupts:
        st.session_state.pending_interrupt = state.interrupts[0].value["action_requests"][0]
    else:
        st.session_state.pending_interrupt = None
        content = state.values["messages"][-1].content
        if isinstance(content, list):
            content = "\n".join(b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text")
        st.session_state.history.append(("assistant", content))


if st.session_state.pending_interrupt:
    action = st.session_state.pending_interrupt
    st.warning(f"**Approval needed**\n\n**Tool:** `{action['name']}`\n\n**Args:** `{action['args']}`")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(":white_check_mark: Approve", use_container_width=True):
            run_turn(Command(resume={"decisions": [{"type": "approve"}]}))
            st.rerun()
    with col2:
        reason = st.text_input("Reason for rejecting (sent to the model)", key="reject_reason")
        if st.button(":x: Reject", use_container_width=True):
            decision = {"type": "reject", "message": reason or "Rejected by the human reviewer."}
            run_turn(Command(resume={"decisions": [decision]}))
            st.rerun()
else:
    user_input = st.chat_input("Ask the planner...")
    if user_input:
        st.session_state.history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)
        run_turn({"messages": [{"role": "user", "content": user_input}]})
        st.rerun()