import streamlit as st
from utils import load_data


df = load_data("data/processed.csv")


st.title("This is the dashboard page")