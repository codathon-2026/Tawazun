"""The "Check a post" input box, which turns Facebook-styled when it holds a Facebook link
or one of the (Facebook-sourced) example posts.

The styling switch happens in the browser: a small script watches the textarea as you type
or paste and toggles a CSS class, so the banner slides in instantly. Streamlit itself only
learns the text when the box loses focus or "Analyse" is pressed.
"""

import html
import json
import re

import streamlit as st

from functions.common import load_json, t

FB_LINK = re.compile(
    r"(?:https?://)?(?<![\w-])(?:[\w-]+\.)?(?:facebook\.com|fb\.com|fb\.watch|fb\.me)\b\S*", re.I
)
ANY_LINK = re.compile(r"https?://\S+|www\.\S+", re.I)


def _norm(text):
    return " ".join(text.split())


def example_posts():
    """The 'Try an example' posts — all presented as coming from Facebook."""
    return load_json("examples.json")["stage_post"]


def source_of(text):
    if FB_LINK.search(text):
        return "fb_link"
    if _norm(text) in {_norm(p) for p in example_posts().values()}:
        return "fb_example"
    return "text"


def strip_links(text):
    return ANY_LINK.sub("", FB_LINK.sub("", text)).strip()


def _watcher_js():
    examples = json.dumps([_norm(p) for p in example_posts().values()], ensure_ascii=False)
    return f"""
<script>
(function () {{
  if (window.__tzFbWatcher) return;
  window.__tzFbWatcher = true;
  const FB = /(?:^|[\\s/.])(?:facebook\\.com|fb\\.com|fb\\.watch|fb\\.me)\\b/i;
  const EXAMPLES = {examples};
  const norm = s => s.split(/\\s+/).filter(Boolean).join(" ");
  setInterval(function () {{
    const box = document.querySelector(".st-key-postbox");
    const ta = box && box.querySelector("textarea");
    if (!ta) return;
    const v = norm(ta.value);
    box.classList.toggle("tz-fb", FB.test(" " + v) || EXAMPLES.includes(v));
  }}, 120);
}})();
</script>"""


def render():
    st.markdown(f"**{t('post_label')}**")
    with st.container(key="postbox"):
        st.markdown(
            '<div class="tz-fb-banner"><span class="tz-fb-logo">f</span>'
            f'<span class="tz-fb-word">Facebook</span>'
            f'<span class="tz-fb-meta">{t("fb_banner")} · 🌐 {t("fb_public")}</span></div>',
            unsafe_allow_html=True,
        )
        st.text_area(
            t("post_label"), key="post_text", height=150,
            placeholder=t("post_placeholder"), label_visibility="collapsed",
        )
    # Kept in the sidebar so the invisible element adds no gap under the box.
    st.sidebar.html(_watcher_js(), unsafe_allow_javascript=True)


def fb_post_card(post_lang):
    """A Facebook-style card showing the post 'retrieved' from a link (it is the stage post)."""
    page = load_json("examples.json")["fb_page"][post_lang]
    text = html.escape(example_posts()[post_lang])
    return (
        '<div class="tz-fb-post">'
        f'<div class="hd"><span class="tz-fb-logo sm">f</span><div><b>{html.escape(page["name"])}</b>'
        f'<div class="meta">{html.escape(page["time"])} · 🌐</div></div></div>'
        f'<p>{text}</p><div class="ft">{html.escape(page["stats"])}</div></div>'
    )
