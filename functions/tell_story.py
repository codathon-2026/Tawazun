"""Feature 07 — Al-Hakeem, the Libyan Arabic story companion.

The one live feature. Two modes:
  * ready prompts (two buttons): prewritten prompt -> fake thinking -> prewritten reply
  * the chat box: sent live to deepseek-chat, using the API key from the sidebar
"""

import time

import streamlit as st
from openai import OpenAI

from functions.common import kicker, lang, load_json, t, typewriter

DEEPSEEK_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
HISTORY_TURNS = 10
AVATARS = {"user": "🙂", "assistant": "🪔"}


def _system_prompt():
    stories = load_json("stories.json")
    text = "\n\n".join(f'{s["title"]}: {s["text"]}' for lng in ("ar", "en") for s in stories[lng])
    return load_json("prompts.json")["hakeem_system"].replace("{stories}", text)


def _live_reply(api_key):
    """Stream a reply from DeepSeek for the conversation so far."""
    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_URL)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.hakeem_msgs
        if m["kind"] != "notice"
    ][-HISTORY_TURNS:]
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": _system_prompt()}] + history,
        temperature=0.8,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def _show(msg):
    with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
        if msg["kind"] == "notice":
            st.info(msg["content"], icon="🔑")
        else:
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                st.caption(t("live_badge") if msg["kind"] == "live" else t("canned_badge"))


def _add(role, content, kind):
    msg = {"role": role, "content": content, "kind": kind}
    st.session_state.hakeem_msgs.append(msg)
    return msg


def render():
    if "hakeem_msgs" not in st.session_state:
        st.session_state.hakeem_msgs = []

    head, clear = st.columns([5, 1], vertical_alignment="bottom")
    with head:
        kicker(t("hakeem_feature"))
        st.subheader(f'🪔 {t("hakeem_title")}')
    with clear:
        if st.button(t("hakeem_clear"), key="hakeem_clear", width="stretch"):
            st.session_state.hakeem_msgs = []
    st.caption(t("hakeem_sub"))

    box = st.container(height=340, border=True)
    with box:
        hint = st.empty()
        if not st.session_state.hakeem_msgs:
            hint.caption(t("hakeem_empty"))
        for msg in st.session_state.hakeem_msgs:
            _show(msg)

    canned = load_json("prompts.json")["canned"][lang()]
    c_input, c_b1, c_b2 = st.columns([6, 2, 2], vertical_alignment="bottom")
    with c_b1:
        b1 = st.button(canned[0]["button"], key="canned_0", width="stretch")
    with c_b2:
        b2 = st.button(canned[1]["button"], key="canned_1", width="stretch")
    with c_input:
        typed = st.chat_input(t("hakeem_input"), key="hakeem_input")

    pressed = canned[0] if b1 else canned[1] if b2 else None
    if pressed or typed:
        hint.empty()

    with box:
        if pressed:
            _show(_add("user", pressed["prompt"], "canned"))
            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                with st.spinner(t("hakeem_thinking")):
                    time.sleep(1.6)
                st.write_stream(typewriter(pressed["reply"]))
                st.caption(t("canned_badge"))
            _add("assistant", pressed["reply"], "canned")

        elif typed:
            _show(_add("user", typed, "live"))
            api_key = st.session_state.get("api_key", "").strip()
            if not api_key:
                _show(_add("assistant", t("hakeem_no_key"), "notice"))
                return
            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                try:
                    with st.spinner(t("hakeem_thinking")):
                        stream = _live_reply(api_key)
                        first = next(stream, "")
                    reply = st.write_stream(_chain(first, stream))
                except Exception as e:  # network, bad key, rate limit — keep the demo standing
                    st.error(t("hakeem_error", err=type(e).__name__), icon="⚠️")
                    return
                st.caption(t("live_badge"))
            _add("assistant", reply, "live")


def _chain(first, rest):
    if first:
        yield first
    yield from rest
