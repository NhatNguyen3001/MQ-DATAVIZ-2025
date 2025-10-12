# import libraries
import streamlit as st
from utils import load_data
import numpy as np
from typing import Tuple
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
import pycountry

from utils import ensure_columns, available_years, fmt_ug, risk_badge, _risk_tier, iso3_to_numeric, _status_style
from utils import set_page_background
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

set_page_background(
    "img/dark_bg.png",
    "img/dark_bg.png",
    size="cover",
    position="center center",
    opacity=0.9
)

st.markdown("""
    <style>
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    /* Metric card labels and values */
    [data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    [data-testid="stMetricValue"] {
        color: white !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: white !important;
    }
    
    /* Captions */
    .stCaptionContainer, .caption {
        color: white !important;
    }
    
    [data-testid="stCaptionContainer"] {
        color: white !important;
    }
    
    /* Alternative caption selector */
    .element-container .caption {
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: white !important;
    }
    
    /* Tab content */
    .stTabs [data-baseweb="tab-panel"] {
        color: white !important;
    }
    
    /* Dataframe background using Glide Data Grid CSS variables */
    .stDataFrameGlideDataEditor {
        --gdg-bg-cell: rgba(43, 50, 77, 0.8) !important;
        --gdg-bg-cell-medium: rgba(43, 50, 77, 0.85) !important;
        --gdg-bg-header: rgba(43, 50, 77, 0.95) !important;
        --gdg-bg-header-has-focus: rgba(43, 50, 77, 0.95) !important;
        --gdg-bg-header-hovered: rgba(43, 50, 77, 1) !important;
        --gdg-text-dark: white !important;
        --gdg-text-medium: rgba(255, 255, 255, 0.9) !important;
        --gdg-text-light: rgba(255, 255, 255, 0.7) !important;
        --gdg-text-header: white !important;
        --gdg-border-color: rgba(255, 255, 255, 0.2) !important;
        --gdg-horizontal-border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Canvas background */
    .stDataFrameGlideDataEditor canvas {
        background-color: rgba(43, 50, 77, 0.8) !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

def times_above_who(value, pollutant_col):
    if pd.isna(value):
        return "—"
    limit = WHO_LIMITS[pollutant_col]
    return f"{value/limit:.1f}× WHO"

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

# Annual mean
annual_mean = float(np.nanmean(dff[pollutant_col].values)) if not dff.empty else np.nan

# % of countries exceeding WHO guideline
country_mean = (
    dff.groupby("country_name", dropna=True)[pollutant_col]
    .mean()
    .dropna()
)
if country_mean.empty:
    pct_exceed = np.nan
else:
    limit = WHO_LIMITS[pollutant_col]
    pct_exceed = 100.0 * (country_mean > limit).mean()

# Calculate worst performer
idx_max = dff[pollutant_col].idxmax()
worst_country = dff.at[idx_max, "country_name"] if pd.notna(idx_max) else None
worst_value = dff.at[idx_max, pollutant_col] if pd.notna(idx_max) else np.nan
worst_year = int(dff.at[idx_max, "year"]) if pd.notna(idx_max) else None

# Calculate best performer
idx_min = dff[pollutant_col].idxmin()
best_country = dff.at[idx_min, "country_name"] if pd.notna(idx_min) else None
best_value = dff.at[idx_min, pollutant_col] if pd.notna(idx_min) else np.nan
best_year = int(dff.at[idx_min, "year"]) if pd.notna(idx_min) else None

# Worst case concentration 
worst_case_value = float(np.nanmax(dff[pollutant_col].values))

# Best case concentration
best_case_value = float(np.nanmin(dff[pollutant_col].values))

# KPI Cards (1 row, 6 cards)
spacerL, col1, col2, col3, spacerR = st.columns([1, 2, 2, 2, 1])
spacerL, col4, col5, col6, spacerR = st.columns([1, 2, 2, 2, 1])

with stylable_container(key="kpi_row", css_styles="""
    { padding: 0.25rem 0; }
"""):
    # Annual Mean Card
    with col1:
        badge = risk_badge(annual_mean, pollutant_col)
        st.metric(
            label=f"Annual Mean ({POLLUTANT_LABEL[pollutant_col]})",
            value=fmt_ug(annual_mean),
            delta=badge
        )
        st.caption(f"WHO annual guideline ≤ {WHO_LIMITS[pollutant_col]:.0f} µg/m³ • Region: {selected_region}")

    # % Exceeding WHO Card
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

    # Worst Performer Card
    with col3:
        st.metric(
            label="Worst Performer",
            value="—" if worst_country is None else f"{dff.at[idx_max, 'iso3']}",
            delta="—" if pd.isna(worst_value) else f"{fmt_ug(worst_value)} • {times_above_who(worst_value, pollutant_col)}"
        )
        if worst_year:
            st.caption(f"{worst_country or '—'} • {POLLUTANT_LABEL[pollutant_col]}, Year: {worst_year if worst_year is not None else '—'}")

    # Best Performer Card 
    with col4:
        st.metric(
            label="Best Performer",
            value="—" if best_country is None else f"{dff.at[idx_min, 'iso3']}",
            delta="—" if pd.isna(best_value) else f"{fmt_ug(best_value)} • {risk_badge(best_value, pollutant_col)}"
        )
        if best_year:
            st.caption(f"{best_country or '—'} • {POLLUTANT_LABEL[pollutant_col]}, Year: {best_year if best_year is not None else '—'}")
        

    # Worst Concentration Card
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

    # Best Case Concentration Card
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

# Visual 1: Trend Line Chart
def make_trend_chart(df_scope, selected_region, pollutant_col, pollutant_label, who_limit):
    trend = (df_scope.groupby("year")[pollutant_col]
             .mean().reset_index().rename(columns={pollutant_col: "value"}).sort_values("year"))
    if trend.empty:
        return alt.Chart(pd.DataFrame({"note":["No data"]})).mark_text(size=16).encode(text="note")

    # --- y-axis domain: start at 0, add ~10% headroom above max ---
    ymax = float(trend["value"].max())
    y_top = 0.0 if np.isnan(ymax) else ymax * 1.1  # headroom
    if y_top == 0.0:  # all zeros/NaNs
        y_top = who_limit * 1.2

    base = alt.Chart(trend).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y(
            "value:Q",
            title=f"{pollutant_label} (µg/m³)",          # if fonts glitch, use "µg/m3"
            scale=alt.Scale(domain=(0, y_top))            # <-- key fix
        ),
        tooltip=[alt.Tooltip("year:O", title="Year"),
                 alt.Tooltip("value:Q", title=f"{pollutant_label} (mean)", format=",.1f")]
    )

    line = base.mark_line(point=True, color='white')
    who_rule = alt.Chart(pd.DataFrame({"y":[who_limit]})).mark_rule(strokeDash=[4,4], color='white').encode(y="y:Q")
    who_label = alt.Chart(pd.DataFrame({"y":[who_limit], "text":[f"WHO ≤ {who_limit:.0f} µg/m³"]})) \
        .mark_text(align="left", dx=6, dy=-6, fontSize=11, color='white').encode(y="y:Q", text="text:N")

    return (line + who_rule + who_label).properties(height=300).configure(
        background='rgba(43, 50, 77, 0.8)').interactive()

# Visual 2: choropleth map
@st.cache_data(show_spinner=False)
def _world_topo():
    return vega_data.world_110m.url  # topojson with 'countries' object

def make_choropleth(df_scope, pollutant_col, pollutant_label, selected_region):
    country_mean = (df_scope.groupby(["iso3","country_name"])[pollutant_col]
                   .mean().reset_index().rename(columns={pollutant_col:"value"}).dropna(subset=["iso3","value"]))
    if country_mean.empty:
        return alt.Chart(pd.DataFrame({"note":["No data"]})).mark_text(size=16).encode(text="note")

    country_mean["WHO status"] = country_mean["value"].apply(lambda v: _risk_tier(v, pollutant_col))
    country_mean["iso_numeric"] = country_mean["iso3"].apply(iso3_to_numeric)
    country_mean = country_mean.dropna(subset=["iso_numeric"]).astype({"iso_numeric": int})

    countries = alt.topo_feature(_world_topo(), "countries")

    chart = (
        alt.Chart(countries).mark_geoshape(stroke="#ffffff", strokeWidth=0.25)
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(country_mean, "iso_numeric", ["value","iso3","country_name","WHO status"])
        )
        .encode(
            color=alt.Color(
                "WHO status:N",
                title="WHO Risk Status",
                scale=alt.Scale(
                    domain=["Safe","Moderate","High","Very high"],
                    range=["#31a354","#feb24c","#f03b20","#bd0026"]
                ),
                legend=alt.Legend(orient="bottom")
            ),
            tooltip=[
                alt.Tooltip("country_name:N", title="Country"),
                alt.Tooltip("iso3:N", title="ISO3"),
                alt.Tooltip("value:Q", title=f"{pollutant_label} (mean)", format=",.1f"),
                alt.Tooltip("WHO status:N", title="WHO Status")
            ]
        )
        .properties(height=360)
        .configure(background='rgba(43, 50, 77, 0.8)')
        .project(type="equalEarth", scale=150, center=[0, 20])
        
    )
    return chart

# Visual 3: Bar charts (Top 10 best/worst)
def make_top5_bars(df_scope, pollutant_col, pollutant_label, selected_region):
    stats = (
        df_scope.groupby(["iso3","country_name"])[pollutant_col]
        .mean().reset_index()
        .rename(columns={pollutant_col:"value"})
        .dropna(subset=["iso3","value"])
    )
    if stats.empty:
        nd = alt.Chart(pd.DataFrame({"note":["No data"]})).mark_text(size=16).encode(text="note")
        return nd, nd

    stats["WHO status"] = stats["value"].apply(lambda v: _risk_tier(v, pollutant_col))

    def bar(df_in, title, order="descending"):
        df = df_in.copy()
        df["iso3"] = df["iso3"].astype(str)
        return (
            alt.Chart(df).mark_bar().encode(
                x=alt.X("value:Q", title=f"{pollutant_label} (µg/m³, mean)"),
                y=alt.Y(
                    "iso3:N",
                    sort=alt.SortField(field="value", order=order),  # <-- key change
                    title="ISO3"
                ),
                color=alt.Color(
                    "WHO status:N",
                    scale=alt.Scale(
                        domain=["Safe","Moderate","High","Very high"],
                        range=["#31a354","#feb24c","#f03b20","#bd0026"]
                    ),
                    legend=alt.Legend(orient="bottom")
                ),
                tooltip=[
                    alt.Tooltip("country_name:N", title="Country"),
                    alt.Tooltip("iso3:N", title="ISO3"),
                    alt.Tooltip("value:Q", title=f"{pollutant_label} (mean)", format=",.1f"),
                    alt.Tooltip("WHO status:N")
                ],
            ).properties(height=360).configure(
                background='rgba(43, 50, 77, 0.8)'
            )
        )

    chart_hi = bar(stats.nlargest(5, "value"), "Top 5 Highest", order="descending")
    chart_lo = bar(stats.nsmallest(5, "value"), "Top 5 Lowest", order="ascending")  

    return chart_hi, chart_lo

# RENDER VISUALS

# Prepare charts
trend_chart = make_trend_chart(
    dff, selected_region, pollutant_col,
    POLLUTANT_LABEL[pollutant_col], WHO_LIMITS[pollutant_col]
)
map_chart = make_choropleth(
    dff, pollutant_col, POLLUTANT_LABEL[pollutant_col], selected_region
)

# Get both Top-5 charts
chart_hi, chart_lo = make_top5_bars(
    dff, pollutant_col, POLLUTANT_LABEL[pollutant_col], selected_region
)

c1, c2 = st.columns([1.5,1], gap="large")

with c1:
    st.markdown(f'<p style="color: white; font-weight: bold;">{POLLUTANT_LABEL[pollutant_col]} Distribution in {selected_region}</p>', 
    unsafe_allow_html=True)
    st.altair_chart(map_chart.properties(height=500), use_container_width=True)

with c2:
    st.markdown(f'<p style="color: white; font-weight: bold;">{POLLUTANT_LABEL[pollutant_col]} Trends in {selected_region}</p>', 
    unsafe_allow_html=True)
    st.altair_chart(trend_chart.properties(height=500), use_container_width=True)


c3, c4 = st.columns(2, gap="small")

# Col 3: Top 5 Bars (tabs)
with c3:
    st.markdown(f'<p style="color: white; font-weight: bold;">Top 5 Highest {POLLUTANT_LABEL[pollutant_col]} in {selected_region}</p>', 
    unsafe_allow_html=True)
    st.altair_chart(chart_hi.properties(height=360), use_container_width=True)
    
    # tab1, tab2 = st.tabs([
    #     f"🌋 Top 5 Highest {POLLUTANT_LABEL[pollutant_col]} in {selected_region}",
    #     f"🍃 Top 5 Lowest {POLLUTANT_LABEL[pollutant_col]} in {selected_region}"
    # ])
    
    # with tab1:
    #     st.altair_chart(chart_hi.properties(height=300), use_container_width=True)
    # with tab2:
    #     st.altair_chart(chart_lo.properties(height=300), use_container_width=True)

# Col 4 — Table (+ download)
with c4:
    st.markdown(f'<p style="color: white; font-weight: bold;">Top 5 Lowest {POLLUTANT_LABEL[pollutant_col]} in {selected_region}</p>', 
    unsafe_allow_html=True)
    st.altair_chart(chart_lo.properties(height=360), use_container_width=True)
    # st.markdown(f'<p style="color: white; font-weight: bold;">Country-Level {POLLUTANT_LABEL[pollutant_col]} — Mean across Selected Years ({selected_region})</p>', 
    #             unsafe_allow_html=True)
    # col_name = f"{POLLUTANT_LABEL[pollutant_col]} (µg/m³) — mean"

    # table_df = (
    #     dff.groupby(["iso3", "country_name"])[pollutant_col]
    #     .mean()
    #     .reset_index()
    #     .rename(columns={pollutant_col: col_name})
    #     .sort_values(by=col_name, ascending=True)
    # )
    # table_df["WHO status"] = table_df[col_name].apply(lambda v: _risk_tier(v, pollutant_col))

    # styler = (
    #    table_df.style
    #     .format({col_name: "{:.2f}"})
    #     .set_table_styles([
    #         {"selector": "tbody tr:nth-child(odd)", "props": "background-color: rgba(43, 50, 77, 0.8); color: white;"},
    #         {"selector": "tbody tr:nth-child(even)", "props": "background-color: rgba(43, 50, 77, 0.9); color: white;"},
    #         {"selector": "th.col_heading, th.row_heading", "props": "background-color: rgba(43, 50, 77, 0.95); font-weight: 600; color: white;"},
    #         {"selector": "thead th", "props": "background-color: rgba(43, 50, 77, 0.95); font-weight: 700; color: white;"},
    #         {"selector": "", "props": "background-color: rgba(43, 50, 77, 0.8);"},  # Overall table background
    #     ])
    #     .applymap(_status_style, subset=["WHO status"])
    #     .bar(subset=[col_name], color="#cfe6ff")
    # )

    # st.dataframe(styler, use_container_width=True, hide_index=True, height=360)

st.markdown(f'<p style="color: white; font-weight: bold;">Country-Level {POLLUTANT_LABEL[pollutant_col]} — Mean across Selected Years ({selected_region})</p>', 
                unsafe_allow_html=True)
col_name = f"{POLLUTANT_LABEL[pollutant_col]} (µg/m³) — mean"

table_df = (
    dff.groupby(["iso3", "country_name"])[pollutant_col]
    .mean()
    .reset_index()
    .rename(columns={pollutant_col: col_name})
    .sort_values(by=col_name, ascending=True)
)
table_df["WHO status"] = table_df[col_name].apply(lambda v: _risk_tier(v, pollutant_col))

styler = (
    table_df.style
    .format({col_name: "{:.2f}"})
    .set_table_styles([
        {"selector": "tbody tr:nth-child(odd)", "props": "background-color: rgba(43, 50, 77, 0.8); color: white;"},
        {"selector": "tbody tr:nth-child(even)", "props": "background-color: rgba(43, 50, 77, 0.9); color: white;"},
        {"selector": "th.col_heading, th.row_heading", "props": "background-color: rgba(43, 50, 77, 0.95); font-weight: 600; color: white;"},
        {"selector": "thead th", "props": "background-color: rgba(43, 50, 77, 0.95); font-weight: 700; color: white;"},
        {"selector": "", "props": "background-color: rgba(43, 50, 77, 0.8);"},  # Overall table background
    ])
    .applymap(_status_style, subset=["WHO status"])
    .bar(subset=[col_name], color="#cfe6ff")
)

st.dataframe(styler, use_container_width=True, hide_index=True, height=360)