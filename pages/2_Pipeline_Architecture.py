from pathlib import Path

import streamlit as st

import cinematch_embed


st.set_page_config(
    page_title="CineMatch | Research Portfolio & Recommendation Engine",
    page_icon=str((Path(__file__).resolve().parent.parent / "cm_favicon.svg")),
    layout="wide",
    initial_sidebar_state="collapsed",
)

cinematch_embed.apply_streamlit_chrome_hiding_css(hide_sidebar=False)
cinematch_embed.render(selected_tab="pipeline", height=2600)
