import streamlit as st
from streamlit_extras.stylable_container import stylable_container


def load_main_page():
    with stylable_container(key ="info_container", css_styles="""{background-color: #3A3C5E;}"""):
        st.markdown("# :white[PhonePe Data Visualization and Exploration]")

    pass

st.set_page_config(layout="wide", page_title="Phonepe Data Visuvalization")
load_main_page()

