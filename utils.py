import streamlit as st
import pandas as pd


@st.cache_data
def load_data(df):
    data = pd.read_csv(df)
    return data

def logo_config():
    st.logo("img/short_logo.png")
    

    

    