"""Feature 02 — Source checker.

Demo: prewritten source cues for the stage post, plus generic places to check
(data/sources.json).
"""

import html

import streamlit as st

from functions.common import card, kicker, load_json


def render(post_lang):
    s = load_json("examples.json")["analysis"][post_lang]["source"]
    kicker(s["kicker"])
    st.subheader(s["heading"])

    rows = "".join(
        f'<div class="tz-cue"><b>{html.escape(c["label"])}</b>'
        f'<span class="{"flag" if c["flag"] else ""}">{"⚠️ " if c["flag"] else ""}{html.escape(c["value"])}</span></div>'
        for c in s["cues"]
    )
    card(rows)

    st.markdown(f"**{s['where_heading']}**")
    places = load_json("sources.json")[post_lang]
    cols = st.columns(2)
    for i, p in enumerate(places):
        with cols[i % 2]:
            card(
                f'<h4>{p["emoji"]} {html.escape(p["name"])}</h4><p class="tz-muted">{html.escape(p["why"])}</p>',
                delay=0.06 * i,
            )
