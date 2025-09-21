import streamlit as st
import pandas as pd


@st.cache_data
def load_data(df, sheet_name):
    data = pd.read_excel(df, sheet_name=sheet_name)
    return data

def logo_config():
    st.logo("img/short_logo.png")
    

    

    