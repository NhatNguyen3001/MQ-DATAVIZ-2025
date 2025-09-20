import streamlit as st
from utils import logo_config
from navigation import navigation_bar

st.set_page_config(page_title="DataViz_2025", page_icon="img/short_logo.png", layout="wide", initial_sidebar_state="auto")

navigation_bar()
logo_config()
