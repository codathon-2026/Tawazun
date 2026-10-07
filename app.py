"""Tawazun — demo build for AI4LY.

A "wax sculpture": it looks like the real product, but everything except Al-Hakeem's
chat box is prewritten (see data/). Run with:  streamlit run app.py
"""

import html
import time

import streamlit as st

from functions import (
    analyze_impact,
    analyze_post,
    check_source,
    coach_response,
    post_box,
    simulate_post,
    tell_story,
    track_mood,
)
from functions.common import (
    detect_lang,
    fake_think,
    inject_css,
    kicker,
    lang,
    scale_logo,
    switch_lang,
    t,
)

st.set_page_config(page_title="Tawazun · توازن", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")


def lang_button(key):
    st.button(t("lang_button"), key=key, on_click=switch_lang, icon="🌐")


def sign_out():
    keep = lang()
    st.session_state.clear()
    st.session_state.lang = keep


# ---------------------------------------------------------------- login

def login_page(slot):
    with slot.container(key="page_login"):
        _, right = st.columns([5, 1])
        with right:
            lang_button("lang_login")

        _, mid, _ = st.columns([1, 1.25, 1])
        with mid:
            st.markdown(
                f'<div class="tz-hero">{scale_logo(96, beam_color="#FFFFFF")}'
                f'<h1 class="tz-wordmark" style="font-size:3rem">{t("app_name")} '
                f'<span class="tz-wordmark-alt" style="font-size:1.4rem">{t("app_name_alt")}</span></h1>'
                f'<div class="tz-kicker">{t("tagline")}</div>'
                f'<p>{t("login_sub")}</p></div>',
                unsafe_allow_html=True,
            )

            with st.form("login", clear_on_submit=True, border=True):
                user = st.text_input(t("username"))
                st.text_input(t("password"), type="password")  # accepted, never stored or checked
                go = st.form_submit_button(t("login_btn"), type="primary", width="stretch")
            st.caption(t("login_hint"))

            points = "".join(f"<li>{html.escape(p)}</li>" for p in t("privacy_points"))
            open_q, close_q = ("«", "»") if lang() == "ar" else ("“", "”")
            st.markdown(
                f'<div class="tz-login-quote"><div class="q">{open_q}{t("quote")}{close_q}</div>'
                f'<div class="src">— {t("quote_src")}</div></div>'
                f'<div class="tz-privacy"><div class="ttl">🔒 {t("privacy_title")}</div><ul>{points}</ul></div>',
                unsafe_allow_html=True,
            )

        if go:
            st.session_state.user = user.strip() or t("guest")
            st.session_state.page = "splash"
            st.rerun()


# ---------------------------------------------------------------- splash (login -> app transition)

def splash_page(slot):
    with slot.container(key="page_splash"):
        st.markdown(
            f'<div class="tz-splash">{scale_logo(180, beam_color="#FFFFFF")}'
            f'<div class="msg">{t("splash")}</div></div>',
            unsafe_allow_html=True,
        )
    time.sleep(1.9)
    st.session_state.page = "main"
    st.rerun()


# ---------------------------------------------------------------- main app

def sidebar():
    with st.sidebar:
        st.markdown(scale_logo(80, animate=False), unsafe_allow_html=True)
        st.markdown(f"**{t('sidebar_live')}**")
        st.text_input(t("key_label"), type="password", key="api_key", help=t("key_help"))
        if st.session_state.get("api_key", "").strip():
            st.success(t("key_ok"), icon="🟢")
        else:
            st.caption(f"⚪ {t('key_missing')}")
        st.divider()
        st.caption(f"🧪 {t('demo_badge')}")
        st.button(t("logout"), on_click=sign_out, icon="🚪", key="logout")


def check_post_tab():
    kicker(t("tab_features")[0])
    st.header(t("tab1_title"))
    st.write(t("tab1_sub"))

    post_box.render()

    def use_example():
        st.session_state.post_text = post_box.example_posts()[lang()]

    b1, b2, _ = st.columns([1.3, 1.3, 4])
    with b1:
        analyse = st.button(t("analyse_btn"), type="primary", icon="🔍", width="stretch")
    with b2:
        st.button(t("example_btn"), on_click=use_example, width="stretch")

    if analyse:
        text = st.session_state.post_text.strip()
        if not text:
            st.warning(t("empty_warning"))
            st.session_state.pop("analysed_lang", None)
        else:
            content = post_box.strip_links(text)
            # A bare Facebook link: pretend to fetch the post (it is the stage post, in the UI language).
            fetched = post_box.source_of(text) == "fb_link" and not content
            steps = ([t("fetch_step")] if fetched else []) + t("think_steps")
            fake_think(steps, t("think_label"), t("think_done"))
            st.session_state.analysed_lang = lang() if fetched else detect_lang(content or text)
            st.session_state.fetched = fetched
            st.session_state.analysis_run = st.session_state.get("analysis_run", 0) + 1

    post_lang = st.session_state.get("analysed_lang")
    if post_lang:
        direction = "rtl" if post_lang == "ar" else "ltr"
        with st.container(key=f"dir_{direction}_results_{st.session_state.analysis_run}"):
            if st.session_state.get("fetched"):
                kicker(t("fetched_title"))
                st.markdown(post_box.fb_post_card(post_lang), unsafe_allow_html=True)
            left, right = st.columns([1.15, 1], gap="large")
            with left:
                analyze_post.render(post_lang)
            with right:
                check_source.render(post_lang)
            st.divider()
            analyze_impact.render(post_lang)

    st.divider()
    track_mood.render()


def main_page(slot):
    with slot.container(key="page_main"):
        sidebar()

        title, toggle = st.columns([6, 1.4], vertical_alignment="center")
        with title:
            st.markdown(
                f'<div class="tz-header">{scale_logo(84)}<div>'
                f'<h1 class="tz-wordmark" style="font-size:2.3rem">{t("app_name")} '
                f'<span class="tz-wordmark-alt" style="font-size:1.3rem">{t("app_name_alt")}</span></h1>'
                f'<div class="tz-muted">{html.escape(t("welcome", name=st.session_state.get("user", t("guest"))))}'
                f' · {t("tagline")}</div></div></div>',
                unsafe_allow_html=True,
            )
        with toggle:
            lang_button("lang_main")

        tab1, tab2, tab3 = st.tabs(t("tabs"))
        with tab1:
            check_post_tab()
        with tab2:
            simulate_post.render()
            st.divider()
            coach_response.render()
        with tab3:
            tell_story.render()


# ---------------------------------------------------------------- router

page = st.session_state.get("page", "login")
inject_css(page)
slot = st.empty()
if page == "login":
    login_page(slot)
elif page == "splash":
    splash_page(slot)
else:
    main_page(slot)
