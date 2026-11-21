from pathlib import Path

import streamlit as st

def load_custom_css():
    css_path = Path(__file__).parent / "styles.css"

    with open(css_path, encoding="utf-8") as file:
        css = file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
