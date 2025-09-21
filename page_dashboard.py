import streamlit as st
from utils import load_data


df = load_data("data/who_ambient_air_quality_database_version_2024.xlsx", "data")


st.title("This is the dashboard page")