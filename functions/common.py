"""Shared helpers: data loading, language, fake "AI thinking", styling."""

import json
import re
import time
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"

# Pitch-deck palette (pulled from the slide XML).
INK = "#142B2E"
FOREST = "#315B4C"
TERRACOTTA = "#C75A4A"
SAGE = "#B7C78A"
SLATE = "#677572"
MIST = "#D8DED3"
PAPER = "#FBFAF6"

# Arabic typeface. Latin text keeps Streamlit's "Source Sans"; Arabic letters (which Source Sans
# lacks) fall through to this font. Loaded from Google Fonts, so it needs internet; without it
# the browser falls back to Tahoma.
ARABIC_FONT = "Noto Kufi Arabic"
ARABIC_FONT_URL = "https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;700;800&display=swap"
ARABIC_FONT_PX = 18  # Arabic UI base size (Streamlit's default is 16px)

ARABIC_CHARS = re.compile(r"[؀-ۿݐ-ݿ]")
LATIN_CHARS = re.compile(r"[A-Za-z]")


@st.cache_data
def _load_json(name, mtime):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def load_json(name):
    """Cached, but re-read whenever the file changes (mtime is part of the cache key)."""
    return _load_json(name, (DATA_DIR / name).stat().st_mtime)


def lang():
    """Interface language: 'ar' (default) or 'en'."""
    return st.session_state.get("lang", "ar")


def t(key, **fmt):
    """Interface string in the current language."""
    value = load_json("ui.json")[lang()][key]
    return value.format(**fmt) if fmt else value


def detect_lang(text):
    """Language of a piece of user text, judged by its script, not by the interface setting."""
    arabic = len(ARABIC_CHARS.findall(text))
    latin = len(LATIN_CHARS.findall(text))
    if arabic == 0 and latin == 0:
        return lang()
    return "ar" if arabic >= latin else "en"


def switch_lang():
    """Button callback. Switching language restarts the app (back to the login page)."""
    new_lang = "en" if lang() == "ar" else "ar"
    st.session_state.clear()
    st.session_state.lang = new_lang


def fake_think(steps, label, done_label, step_seconds=0.7):
    """Animated status box that pretends the AI is working through steps."""
    with st.status(label, expanded=True) as status:
        for step in steps:
            st.write(step)
            time.sleep(step_seconds)
        status.update(label=done_label, state="complete", expanded=False)


def typewriter(text, word_seconds=0.025):
    """Generator for st.write_stream: replays prewritten text word by word."""
    for word in re.split(r"(\s+)", text):
        yield word
        if word.strip():
            time.sleep(word_seconds)


def scale_logo(size=120, beam_color=INK, animate=True):
    """The Tawazun balance mark: a beam that tips and settles level."""
    cls = "tz-beam tz-animate" if animate else "tz-beam"
    return f"""
<svg class="tz-scale" width="{size}" height="{int(size * 0.55)}" viewBox="0 0 120 66" aria-hidden="true">
  <polygon points="60,32 49,62 71,62" fill="{TERRACOTTA}"/>
  <g class="{cls}">
    <rect x="10" y="27" width="100" height="5" rx="2.5" fill="{beam_color}"/>
    <circle cx="20" cy="16" r="9" fill="{SAGE}"/>
    <circle cx="100" cy="16" r="9" fill="{SAGE}"/>
  </g>
</svg>"""


def card(html, delay=0.0, extra_class=""):
    """A white rounded card that fades up into place; `delay` staggers a group of cards."""
    st.markdown(
        f'<div class="tz-card {extra_class}" style="animation-delay:{delay:.2f}s">{html}</div>',
        unsafe_allow_html=True,
    )


def kicker(text):
    """Small uppercase sage label, like 'PROJECT PITCH' on the deck."""
    st.markdown(f'<div class="tz-kicker">{text}</div>', unsafe_allow_html=True)


def inject_css(page):
    """Global styles plus per-page tweaks (dark login, RTL for Arabic)."""
    stack = f'"Source Sans", "Source Sans Pro", "{ARABIC_FONT}", Tahoma, sans-serif'
    css = f"@import url('{ARABIC_FONT_URL}');\n"
    css += f"""
.stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp button, .stApp input, .stApp textarea, .stApp .tz-card, .stApp .tz-kicker {{ font-family: {stack}; }}
"""
    css += (ASSETS_DIR / "style.css").read_text(encoding="utf-8")
    if lang() == "ar":
        css += f"html {{ font-size: {ARABIC_FONT_PX}px; }}\n"
        css += """
.stMainBlockContainer, section[data-testid="stSidebar"] { direction: rtl; }
.stMainBlockContainer p, .stMainBlockContainer h1, .stMainBlockContainer h2,
.stMainBlockContainer h3, .stMainBlockContainer li, section[data-testid="stSidebar"] p { text-align: right; }
.tz-kicker { letter-spacing: 0; font-size: .86rem; text-align: right; }  /* letter-spacing breaks Arabic joining */
.stMainBlockContainer [class*="st-key-dir_ltr"] .tz-kicker { text-align: left; }
"""
    if page in ("login", "splash"):
        css += f"""
.stApp {{ background: {INK}; }}
.stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3 {{ color: #FFFFFF; }}
"""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
