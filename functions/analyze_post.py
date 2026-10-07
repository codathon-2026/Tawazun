"""Feature 01 — Misinformation detector.

Demo: whatever is pasted, the result is the prewritten analysis of the stage post
(data/examples.json), in the language the pasted text is written in.
"""

import html

import streamlit as st

from functions.common import card, kicker, load_json


def get_analysis(post_lang):
    return load_json("examples.json")["analysis"][post_lang]


def render(post_lang):
    a = get_analysis(post_lang)
    kicker(a["kicker"])
    st.subheader(a["heading"])
    st.write(a["summary"])

    for i, sig in enumerate(a["signals"]):
        level = sig["level"]
        card(
            f'<h4>{html.escape(sig["label"])}'
            f'<span class="tz-chip {level}">{a["level_names"][level]}</span></h4>'
            f'<p class="tz-quote">{html.escape(sig["quote"])}</p>'
            f'<p>{html.escape(sig["explain"])}</p>',
            delay=0.08 * i,
        )

    card(
        f'<h4>⚖️ {a["uncertainty_title"]}</h4><p>{html.escape(a["uncertainty"])}</p>',
        delay=0.08 * len(a["signals"]),
        extra_class="tz-tint",
    )
