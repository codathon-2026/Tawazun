"""Feature 06 — Hate-speech response coach.

Demo: one fictional hostile comment and three prewritten ways to respond.
"""

import html

import streamlit as st

from functions.common import card, kicker, lang, load_json, t


def render():
    c = load_json("examples.json")["coach"][lang()]

    kicker(t("coach_feature"))
    st.subheader(t("coach_title"))
    st.caption(t("coach_sub"))

    card(
        f'<p><span class="tz-avatar">🙂</span><b>{html.escape(c["context_user"])}</b></p>'
        f'<p>{html.escape(c["context_comment"])}</p>',
        extra_class="tz-post",
    )
    card(
        f'<p><span class="tz-avatar">U</span><b>{html.escape(c["hostile_user"])}</b></p>'
        f'<p>{html.escape(c["hostile_comment"])}</p>',
        delay=0.1,
        extra_class="tz-hostile",
    )

    cols = st.columns(len(c["options"]))
    for i, (col, opt) in enumerate(zip(cols, c["options"])):
        with col:
            card(
                f'<h4>{opt["emoji"]} {html.escape(opt["label"])}</h4>'
                f'<p class="tz-quote">{html.escape(opt["reply"])}</p>'
                f'<p class="tz-muted"><b>{t("coach_why")}:</b> {html.escape(opt["why"])}</p>',
                delay=0.2 + 0.1 * i,
            )

    avoid = " · ".join(html.escape(a) for a in c["avoid"])
    card(f'<p><b>🚫 {t("coach_avoid_title")}:</b> {avoid}</p>', delay=0.5, extra_class="tz-tint")
