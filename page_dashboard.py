# import libraries
import streamlit as st
from utils import load_data
import numpy as np
from typing import Tuple
import pandas as pd

from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

# set thresholds and labels
WHO_LIMITS = {
    "pm25_concentration": 5.0,   # µg/m³ (annual)
    "pm10_concentration": 15.0,  # µg/m³ (annual)
    "no2_concentration": 10.0,   # µg/m³ (annual)
}
POLLUTANT_LABEL = {
    "pm25_concentration": "PM2.5",
    "pm10_concentration": "PM10",
    "no2_concentration": "NO₂",
}

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

def times_above_who(value, pollutant_col):
    if pd.isna(value):
        return "—"
    limit = WHO_LIMITS[pollutant_col]
    return f"{value/limit:.1f}× WHO"

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

# page title
st.title("🌫️ WHO Ambient Air Quality — Interactive Dashboard")

# load data
df = load_data("data/processed.csv")
ensure_columns(df)

# Coerce types
df["year"] = df["year"].astype(int)
for col in ["pm25_concentration", "pm10_concentration", "no2_concentration"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    
# Filters
st.sidebar.markdown("### Filters")
ymin, ymax = available_years(df)
year_options = sorted(df["year"].unique().tolist())
selected_years = st.sidebar.multiselect(
    "Year(s)", options=year_options, default=year_options,
    help="Pick one or multiple years"
)
if not selected_years:
    st.warning("Select at least one year.")
    st.stop()

regions = ["Global"] + sorted(df["who_region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("WHO Region", options=regions, index=0)

pollutant_friendly = ["PM2.5", "PM10", "NO₂"]
pollutant_choice = st.sidebar.selectbox("Pollutant", pollutant_friendly, index=0)
pollutant_map = {"PM2.5": "pm25_concentration", "PM10": "pm10_concentration", "NO₂": "no2_concentration"}
pollutant_col = pollutant_map[pollutant_choice]

# Apply filters
mask_year = df["year"].isin(selected_years)
mask_region = True if selected_region == "Global" else (df["who_region"] == selected_region)
dff = df.loc[mask_year & mask_region].copy()

# 1) Annual mean (median across all country-year rows in scope)
annual_median = float(np.nanmedian(dff[pollutant_col].values)) if not dff.empty else np.nan

# 2) % of countries exceeding WHO guideline (aggregate by country across selected years with median, then compare)
country_med = (
    dff.groupby("country_name", dropna=True)[pollutant_col]
    .median()
    .dropna()
)
if country_med.empty:
    pct_exceed = np.nan
else:
    limit = WHO_LIMITS[pollutant_col]
    pct_exceed = 100.0 * (country_med > limit).mean()

# 3) Worst performer (country w/ highest concentration; show its year too)
idx_max = dff[pollutant_col].idxmax()
worst_country = dff.at[idx_max, "country_name"] if pd.notna(idx_max) else None
worst_value = dff.at[idx_max, pollutant_col] if pd.notna(idx_max) else np.nan
worst_year = int(dff.at[idx_max, "year"]) if pd.notna(idx_max) else None

# 4) Best performer (country w/ lowest concentration)
idx_min = dff[pollutant_col].idxmin()
best_country = dff.at[idx_min, "country_name"] if pd.notna(idx_min) else None
best_value = dff.at[idx_min, pollutant_col] if pd.notna(idx_min) else np.nan
best_year = int(dff.at[idx_min, "year"]) if pd.notna(idx_min) else None

# 5) Worst case concentration (value only)
worst_case_value = float(np.nanmax(dff[pollutant_col].values))

# 6) Best case concentration (value only)
best_case_value = float(np.nanmin(dff[pollutant_col].values))

# KPI Cards (1 row, 6 cards)
# ----------------------------
st.markdown("### Key Metrics")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with stylable_container(key="kpi_row", css_styles="""
    { padding: 0.25rem 0; }
"""):
    # 1) Annual Mean
    with col1:
        badge = risk_badge(annual_median, pollutant_col)
        st.metric(
            label=f"Annual Mean ({POLLUTANT_LABEL[pollutant_col]})",
            value=fmt_ug(annual_median),
            delta=badge
        )
        st.caption(f"WHO annual guideline ≤ {WHO_LIMITS[pollutant_col]:.0f} µg/m³ • Region: {selected_region}")

    # 2) % Exceeding WHO
    with col2:
        # Color via emoji in delta text; keep consistent thresholds
        if pd.isna(pct_exceed):
            exceed_badge = "⚪ N/A"
        elif pct_exceed < 25:
            exceed_badge = "🟢 Low"
        elif pct_exceed <= 75:
            exceed_badge = "🟡 Mixed"
        else:
            exceed_badge = "🔴 Widespread"
        st.metric(
            label="% Exceeding WHO",
            value="—" if pd.isna(pct_exceed) else f"{pct_exceed:.0f}%",
            delta=exceed_badge
        )
        st.caption(f"Percentage of countries above WHO {POLLUTANT_LABEL[pollutant_col]} limit ({WHO_LIMITS[pollutant_col]:.0f} µg/m³)")

    # 3) Worst Performer
    with col3:
        st.metric(
            label="Worst Performer",
            value="—" if worst_country is None else f"{dff.at[idx_max, 'iso3']}",
            delta="—" if pd.isna(worst_value) else f"{fmt_ug(worst_value)} • {times_above_who(worst_value, pollutant_col)}"
        )
        if worst_year:
            st.caption(f"{POLLUTANT_LABEL[pollutant_col]}, Year: {worst_year}")

    # 4) Best Performer 
    with col4:
        st.metric(
            label="Best Performer",
            value="—" if best_country is None else f"{dff.at[idx_min, 'iso3']}",
            delta="—" if pd.isna(best_value) else f"{fmt_ug(best_value)} • {risk_badge(best_value, pollutant_col)}"
        )
        if best_year:
            st.caption(f"{POLLUTANT_LABEL[pollutant_col]}, Year: {best_year}")

    # 5) Worst Concentration
    with col5:
        st.metric(
            label="Worst Concentration",
            value=fmt_ug(worst_case_value),
            delta=risk_badge(worst_case_value, pollutant_col)
        )
        if worst_year:
            st.caption(f"Max observed • {POLLUTANT_LABEL[pollutant_col]} • Year: {worst_year}")
        else:
            st.caption(f"Max observed • {POLLUTANT_LABEL[pollutant_col]}")

    # 6) Best Case Concentration
    with col6:
        st.metric(
            label="Best Concentration",
            value=fmt_ug(best_case_value),
            delta=risk_badge(best_case_value, pollutant_col)
        )
        if best_year:
            st.caption(f"Min observed • {POLLUTANT_LABEL[pollutant_col]} • Year: {best_year}")
        else:
            st.caption(f"Min observed • {POLLUTANT_LABEL[pollutant_col]}")

# Style all metric cards uniformly
style_metric_cards(
    background_color="#FFFFFF10",  # subtle translucent background for dark mode friendly look
    border_color="#cccccc",
    border_left_color="#4f8bf9",
    box_shadow="0px 0px 6px rgba(0,0,0,0.15)"
)