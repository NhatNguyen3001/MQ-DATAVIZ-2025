import streamlit as st
import pandas as pd
import numpy as np
import pycountry
import base64
import pathlib
from streamlit.components.v1 import html
from pathlib import Path

# Get the project root directory (parent of src folder)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed.csv"
IMG_PATH = PROJECT_ROOT / "img"

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    return data

def logo_config():
    st.logo(IMG_PATH / "short_logo.png")
    
def risk_badge(value, pollutant_col):
    """Return a badge (emoji + label) based on WHO thresholds."""
    x = value
    if np.isnan(x):
        return "⚪ N/A"

    if pollutant_col == "pm25_concentration":
        # 🟢 ≤5 | 🟡 6–15 | 🟠 16–35 | 🔴 >35
        if x <= 5: return "🟢 Safe"
        if x <= 15: return "🟡 Moderate"
        if x <= 35: return "🟠 High"
        return "🔴 Very high"

    if pollutant_col == "pm10_concentration":
        # 🟢 ≤15 | 🟡 16–30 | 🟠 31–50 | 🔴 >50
        if x <= 15: return "🟢 Safe"
        if x <= 30: return "🟡 Moderate"
        if x <= 50: return "🟠 High"
        return "🔴 Very high"

    if pollutant_col == "no2_concentration":
        # 🟢 ≤10 | 🟡 11–20 | 🟠 21–40 | 🔴 >40
        if x <= 10: return "🟢 Safe"
        if x <= 20: return "🟡 Moderate"
        if x <= 40: return "🟠 High"
        return "🔴 Very high"

    return "⚪"

def fmt_ug(value):
    return "—" if pd.isna(value) else f"{value:,.0f} µg/m³"

def ensure_columns(df: pd.DataFrame):
    needed = {
        "who_region", "iso3", "country_name", "year",
        "pm25_concentration", "pm10_concentration", "no2_concentration"
    }
    missing = [c for c in needed if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

def available_years(df):
    y = df["year"].dropna().astype(int)
    return int(y.min()), int(y.max())

def iso3_to_numeric(iso3: str):
    """Map ISO3 -> ISO numeric (for world topo join)."""
    try:
        c = pycountry.countries.get(alpha_3=str(iso3))
        return None if c is None else int(c.numeric)
    except Exception:
        return None

def _risk_tier(value: float, pollutant_col: str) -> str:
    """WHO-based risk label (same as your cards)."""
    if pd.isna(value):
        return "N/A"
    if pollutant_col == "pm25_concentration":
        return "Safe" if value <= 5 else "Moderate" if value <= 15 else "High" if value <= 35 else "Very high"
    if pollutant_col == "pm10_concentration":
        return "Safe" if value <= 15 else "Moderate" if value <= 30 else "High" if value <= 50 else "Very high"
    if pollutant_col == "no2_concentration":
        return "Safe" if value <= 10 else "Moderate" if value <= 20 else "High" if value <= 40 else "Very high"
    return "N/A"

# Styler
def _status_style(val):
    color = {
        "Safe": "#31a354",          # green
        "Moderate": "#feb24c",      # amber
        "High": "#f03b20",          # red
        "Very high": "#bd0026"      # dark red
    }.get(val, "#cccccc")
    return (
        "color: white; "
        f"background-color: {color}; "
        "border-radius: 16px; "
        "padding: 2px 10px; "
        "text-align: center;"
    ) if val in {"Safe","Moderate","High","Very high"} else ""
    
def set_page_background(light_img: str,
                        dark_img: str,
                        *,
                        size: str = "cover",
                        position: str = "center center",
                        opacity: float = 1.0,
                        attachment: str = "fixed") -> None:
    """
    Streamlit page background with separate images for light/dark mode.
    Works with local image files (.jpg/.jpeg/.png/.webp).
    Automatically detects system preferences and Streamlit's theme toggle.
    """

    def _mime(path: str) -> str:
        ext = pathlib.Path(path).suffix.lower()
        if ext in {".jpg", ".jpeg"}: return "image/jpeg"
        if ext == ".png":            return "image/png"
        if ext == ".webp":           return "image/webp"
        # fallback
        return "image/jpeg"

    def _b64(path: str) -> str:
        return base64.b64encode(open(path, "rb").read()).decode("utf-8")

    light_b64, dark_b64 = _b64(light_img), _b64(dark_img)
    light_mime, dark_mime = _mime(light_img), _mime(dark_img)

    css = f"""
    <style>
      .stApp {{ background: transparent; }}

      /* Base (light) - default */
      .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: url("data:{light_mime};base64,{light_b64}") no-repeat {position} / {size};
        background-attachment: {attachment};
        opacity: {opacity};
        z-index: -1;
      }}

      /* System dark mode preference */
      @media (prefers-color-scheme: dark) {{
        .stApp::before {{
          background-image: url("data:{dark_mime};base64,{dark_b64}");
        }}
      }}

      /* Streamlit theme toggle (data-theme attribute) */
      html[data-theme="dark"] .stApp::before,
      body[data-theme="dark"] .stApp::before,
      :root[data-theme="dark"] .stApp::before,
      [data-theme="dark"] .stApp::before {{
        background-image: url("data:{dark_mime};base64,{dark_b64}") !important;
      }}

      html[data-theme="light"] .stApp::before,
      body[data-theme="light"] .stApp::before,
      :root[data-theme="light"] .stApp::before,
      [data-theme="light"] .stApp::before {{
        background-image: url("data:{light_mime};base64,{light_b64}") !important;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    