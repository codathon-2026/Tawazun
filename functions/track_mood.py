"""Feature 05 — Mood & media tracker (opt-in).

Demo: 14 days of generated sample data. Two separate charts (mood, minutes) rather
than one chart with two y-axes, because the two measures have different scales.
"""

from datetime import date, timedelta

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from functions.common import FOREST, MIST, SLATE, TERRACOTTA, card, kicker, t

HEAVY_MINUTES = 180


@st.cache_data
def sample_history(days=14, seed=7):
    """Fake history in which heavy-news days tend to have lower mood."""
    rng = np.random.default_rng(seed)
    minutes = rng.integers(60, 280, size=days)
    mood = np.clip(np.round(5.2 - minutes / 80 + rng.normal(0, 0.45, size=days)), 1, 5).astype(int)
    today = date.today()
    dates = [today - timedelta(days=days - 1 - i) for i in range(days)]
    return pd.DataFrame({"day": pd.to_datetime(dates), "mood": mood, "minutes": minutes})


def _base(df):
    # Titles are drawn by Streamlit above each chart: Vega titles vanished in the RTL layout.
    return alt.Chart(df, padding={"left": 6, "right": 18, "top": 8, "bottom": 4}).properties(height=170)


def _style(chart):
    return (
        chart.configure_view(stroke=None)
        .configure_axis(labelColor=SLATE, titleColor=SLATE, gridColor=MIST, domainColor=MIST, tickColor=MIST)
    )


def render():
    kicker(t("mood_feature"))
    st.subheader(t("mood_heading"))
    if not st.toggle(t("mood_toggle"), key="mood_on"):
        st.caption(t("mood_off"))
        return

    df = sample_history()
    x = alt.X("day:T", title=None, axis=alt.Axis(format="%d/%m", labelAngle=0, tickCount=7))

    mood = _base(df).mark_line(
        color=FOREST, strokeWidth=2, point=alt.OverlayMarkDef(color=FOREST, size=60, filled=True)
    ).encode(
        x=x,
        y=alt.Y("mood:Q", title=None, scale=alt.Scale(domain=[1, 5]), axis=alt.Axis(tickCount=5)),
        tooltip=[alt.Tooltip("day:T", title=t("day_axis"), format="%d/%m"), alt.Tooltip("mood:Q", title=t("mood_axis"))],
    )

    media = _base(df).mark_bar(
        color=TERRACOTTA, cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=14
    ).encode(
        x=x,
        y=alt.Y("minutes:Q", title=None),
        tooltip=[alt.Tooltip("day:T", title=t("day_axis"), format="%d/%m"), alt.Tooltip("minutes:Q", title=t("media_axis"))],
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{t('mood_chart_title')}**")
        st.altair_chart(_style(mood), width="stretch")
    with c2:
        st.markdown(f"**{t('media_chart_title')}**")
        st.altair_chart(_style(media), width="stretch")

    heavy = df[df.minutes > HEAVY_MINUTES].mood.mean()
    light = df[df.minutes <= HEAVY_MINUTES].mood.mean()
    card(f'<p>💡 {t("mood_nudge", hi=f"{heavy:.1f}", lo=f"{light:.1f}")}</p>', extra_class="tz-tint")
    st.caption(t("mood_privacy"))
