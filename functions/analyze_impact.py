"""Feature 04 — Psychological impact analyzer, plus the "choose a response" step.

Demo: one prewritten paragraph per feeling; the user picks the feeling.
"""

import html

import streamlit as st

from functions.common import card, kicker, load_json


def _pick(options, key):
    """Pills that return the chosen option dict (or None)."""
    labels = {f'{o["emoji"]} {o["label"]}': o for o in options}
    choice = st.pills(" ", list(labels), key=key, label_visibility="collapsed")
    return labels.get(choice)


def render(post_lang):
    a = load_json("examples.json")["analysis"][post_lang]

    feel = a["feel"]
    kicker(feel["kicker"])
    st.subheader(feel["heading"])
    st.caption(feel["prompt"])
    chosen = _pick(feel["options"], key=f"feeling_{post_lang}")
    if chosen:
        card(f'<p>{html.escape(chosen["text"])}</p>', extra_class="tz-tint")

    st.divider()
    nxt = a["next"]
    kicker(nxt["kicker"])
    st.subheader(nxt["heading"])
    st.caption(nxt["prompt"])
    step = _pick(nxt["options"], key=f"next_{post_lang}")
    if step:
        card(f'<h4>{step["emoji"]} {html.escape(step["label"])}</h4><p>{html.escape(step["text"])}</p>')
