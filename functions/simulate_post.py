"""Feature 03 — Post simulator: a short quiz on spotting manipulation techniques.

Demo: three prewritten fictional posts (data/examples.json -> quiz).
"""

import html

import streamlit as st

from functions.common import card, kicker, lang, load_json, t


def _reset():
    st.session_state.quiz_i = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_checked = False


def render():
    quiz = load_json("examples.json")["quiz"][lang()]
    questions, options = quiz["questions"], quiz["options"]
    n = len(questions)
    if "quiz_i" not in st.session_state:
        _reset()

    kicker(t("quiz_feature"))
    st.subheader(t("quiz_title"))

    i = st.session_state.quiz_i
    if i >= n:
        st.progress(1.0)
        card(f'<h4>🏁 {t("quiz_done", score=st.session_state.quiz_score, n=n)}</h4>', extra_class="tz-tint")
        st.button(t("quiz_restart"), on_click=_reset, key="quiz_restart")
        return

    q = questions[i]
    st.progress(i / n, text=t("quiz_progress", i=i + 1, n=n))
    st.caption(t("quiz_sub"))
    card(f'<p>{html.escape(q["post"])}</p>', extra_class="tz-post")

    choice = st.radio(" ", options, index=None, key=f"quiz_choice_{i}", label_visibility="collapsed",
                      disabled=st.session_state.quiz_checked)

    if not st.session_state.quiz_checked:
        if st.button(t("quiz_check"), type="primary", key=f"quiz_check_{i}"):
            if choice is None:
                st.warning(t("quiz_pick"))
            else:
                st.session_state.quiz_checked = True
                st.session_state.quiz_correct = options.index(choice) == q["answer"]
                st.session_state.quiz_score += int(st.session_state.quiz_correct)
                st.rerun()
        return

    if st.session_state.quiz_correct:
        st.success(f'{t("quiz_right")} {q["explain"]}', icon="✅")
    else:
        st.error(f'{t("quiz_wrong", answer=options[q["answer"]])}. {q["explain"]}', icon="💡")

    def _next():
        st.session_state.quiz_i += 1
        st.session_state.quiz_checked = False

    st.button(t("quiz_next"), type="primary", on_click=_next, key=f"quiz_next_{i}")
