"""Streamlit chat UI.   Run:  streamlit run ui/app.py      (the API must be running on port 8000)

The UI never imports assistant_core: it only talks to the backend through the HTTP API.
"""
import os
import sys
import time
import uuid
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so "import ui..." works under streamlit

from ui.api_client import AssistantClient
from ui.logic import EXAMPLES, WELCOME, format_sources, status_note, validate_input


def stream_text(text: str):
    """Yield text word by word for a typing animation."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)


st.set_page_config(page_title="FIT Study Assistant", page_icon="🎓")
client = AssistantClient(os.getenv("ASSISTANT_API_URL", "http://127.0.0.1:8000"))

# ---- session state: remembered between reruns of this script ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:12]
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
if "rated" not in st.session_state:
    st.session_state.rated = set()

st.title("🎓 FIT Study Assistant")
if not client.healthy():
    st.error("The assistant backend is not reachable. Start it with: uvicorn assistant_api.main:create_app --factory")

with st.sidebar:
    st.subheader("Try an example")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex
    st.caption("This is an AI assistant. Check important decisions with the Training Office.")

# ---- history -------------------------------------------------------------------
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        raw_sources = m.get("raw_sources")
        if raw_sources:
            with st.expander(f"📚 Sources ({len(raw_sources)})"):
                for s in raw_sources:
                    st.markdown(f"- **`{s['id']}`** – {s['title']}")
        elif m.get("sources"):
            st.caption(m["sources"])
        if m.get("note"):
            st.info(m["note"])
        rid = m.get("request_id")
        if rid and rid not in st.session_state.rated:
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("👍", key=f"up{i}"):
                client.send_feedback(rid, 1)
                st.session_state.rated.add(rid)
                st.toast("Thanks for your feedback!")
            if c2.button("👎", key=f"down{i}"):
                client.send_feedback(rid, -1)
                st.session_state.rated.add(rid)
                st.toast("Thanks — we will look at this answer.")


# ---- new question ----------------------------------------------------------------
question = st.chat_input("Ask one question at a time (fees, offices, or the handbook)…") or st.session_state.pop("pending", None)
if question:
    problem = validate_input(question)
    if problem:
        st.warning(problem)
    else:
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking…"):
            result = client.ask(question, st.session_state.session_id)
        if result.ok:
            with st.chat_message("assistant"):
                st.write_stream(stream_text(result.answer))
            note = status_note(result)
            if question.count("?") > 1:
                multi_tip = "Tip: It looks like you asked multiple questions at once. Try asking one question at a time for a complete answer."
                note = f"{note}\n\n{multi_tip}" if note else multi_tip
            st.session_state.messages.append({
                "role": "assistant",
                "content": result.answer,
                "sources": format_sources(result.sources),
                "raw_sources": result.sources,
                "note": note,
                "request_id": result.request_id,
            })
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {result.error}"})
        st.rerun()