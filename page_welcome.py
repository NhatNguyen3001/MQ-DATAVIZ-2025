import streamlit as st

# title 
st.title("👋 Welcome")

st.write("**Team:** super-viz-ers")
st.write("**Competition:** MQ DataViz 2025")
st.write("**Project:** WHO Ambient Air Quality Dashboard")

st.write(
    """
This app explores the **WHO Ambient Air Quality Database (Jan 2024 update)**.  
It allows you to:
- Compare **PM2.5**, **PM10**, and **NO₂** across regions and years  
- See which countries exceed **WHO guidelines**  
- Identify the **best and worst performers** at a glance
"""
)

c1, c2 = st.columns(2)
with c1:
    st.info("**Data source**: WHO Ambient Air Quality (Jan 2024)")
with c2:
    st.success("**Focus**: Annual means vs WHO guidelines")


st.markdown("---")

# how to use
st.subheader("How to use this app")

st.markdown("""
1. **Choose filters** (left sidebar):
   - **Year(s)**: select one or many years. Charts & table aggregate using **mean** across selected years.
   - **WHO Region**: pick a region or **Global**.
   - **Pollutant**: **PM2.5**, **PM10**, or **NO₂**.
2. **Read the KPI cards** (top of *Dashboard*):
   - **Annual Mean** (WHO-consistent), **% Exceeding WHO**, **Best/Worst Performer (ISO3)**, and **Best/Worst Concentration**.
3. **Explore the visuals**:
   - **Trends**: annual mean over time with a WHO guideline line.
   - **Choropleth Map**: countries colored by **WHO risk status**.
   - **Top 5**: switch tabs for **Highest** / **Lowest** countries.
4. **Scroll to the table**:
   - Country-level **mean** values for the selection with WHO status.
   - Use the **Download CSV** button to export the table.
""")

# tips
with st.expander("Tips & Conventions"):
    st.markdown(
    """
**WHO Annual Mean Guidelines** (µg/m³):  
- PM2.5 ≤ **5**  
- PM10 ≤ **15**  
- NO₂ ≤ **10**

**Risk Status Categories (per pollutant):**

- **PM2.5**  
  - 🟢 Safe: ≤ 5  
  - 🟡 Moderate: 6–15  
  - 🟠 High: 16–35  
  - 🔴 Very High: > 35  

- **PM10**  
  - 🟢 Safe: ≤ 15  
  - 🟡 Moderate: 16–30  
  - 🟠 High: 31–50  
  - 🔴 Very High: > 50  

- **NO₂**  
  - 🟢 Safe: ≤ 10  
  - 🟡 Moderate: 11–20  
  - 🟠 High: 21–40  
  - 🔴 Very High: > 40  

**Cards vs Charts:**  
- KPI cards: show **annual mean** (WHO-consistent) and **extremes** for best/worst.  
- Charts & table: use **mean across selected years**.  
- Best/Worst Performer cards: highlight the **specific year** of occurrence.  

**Data coverage:** Some countries and years have limited measurements. Adjust filters if no data appears.
"""
)

# navigation
st.subheader("Navigation")
st.markdown("""
- **Dashboard** → Filters, KPI cards, trend, map, Top 5, and the country table.  
- **Problem Statement** → What question we’re answering and why it matters.  
- **Credits** → Team **super-viz-ers** acknowledgements & references.
""")

st.markdown("---")
st.caption("Built by **super-viz-ers** for **MQ DataViz 2025** · Data: WHO Ambient Air Quality Database (Jan 2024).")