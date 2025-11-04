import streamlit as st
from utils import logo_config
from navigation import navigation_bar
import numpy as np

st.set_page_config(page_title="MQ DataViz 2025 — Air Quality", page_icon="img/short_logo.png", layout="wide", initial_sidebar_state="auto")

navigation_bar()
logo_config()
