import streamlit as st

st.title("🎯 Problem Statement")

st.markdown(
    """
Air pollution is one of the leading environmental risks to human health, 
with major impacts on mortality, respiratory illnesses, and quality of life.  
According to the World Health Organization (WHO), almost the entire global population 
breathes air that exceeds recommended safety limits.

This app uses the **WHO Ambient Air Quality Database (2024 update)** to explore concentrations of:  
- **PM2.5** (fine particulate matter)  
- **PM10** (coarse particulate matter)  
- **NO₂** (nitrogen dioxide)  

By visualising these pollutants across **regions, years, and countries**, 
we aim to uncover insights into global air quality disparities.
"""
)

st.markdown("## 📊 About the dataset")
st.markdown(
    """
The **WHO Ambient Air Quality Database** has been **updated every 2–3 years since 2011**.  
It compiles annual mean concentrations of PM2.5, PM10, and NO₂ measured worldwide.

- **PM2.5 (Particulate Matter ≤ 2.5µm)**  
  Ultrafine particles that penetrate deep into the lungs and bloodstream.  
  Linked to cardiovascular disease, stroke, and premature death.  

- **PM10 (Particulate Matter ≤ 10µm)**  
  Coarser particles that irritate the respiratory system.  
  Contribute to asthma, chronic bronchitis, and reduced lung function.  

- **NO₂ (Nitrogen Dioxide)**  
  A gas mainly produced by vehicle emissions and fossil fuel combustion.  
  Triggers respiratory issues and is a marker of traffic-related pollution.  
"""
)


st.markdown("## 🌍 Why it matters")
c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.image("img/SDG_3.png", caption="SDG 3: Good Health & Well-Being", use_container_width=True)
    st.markdown(
        """
**How this problem links to SDG 3**
- Tracks **annual mean** PM2.5/PM10/NO₂ vs WHO limits -> evidence for reducing **premature deaths** (SDG 3.9).
- Highlights **high-risk regions/countries** so health agencies can prioritize interventions.
- Trends help assess impact of **clean-air policies** on population exposure over time.
        """
    )

with c2:
    st.image("img/SDG_11.png", caption="SDG 11: Sustainable Cities & Communities", use_container_width=True)
    st.markdown(
        """
**How this problem links to SDG 11**
- Air quality is a critical part of building **sustainable and resilient cities**.  
- Regional/country comparisons reveal **urban air-quality disparities**.  
- Data helps policymakers evaluate progress toward **Target 11.6**: reducing the environmental impact of cities.
        """
    )

with c3:
    st.image("img/SDG_13.png", caption="SDG 13: Climate Action", use_container_width=True)
    st.markdown(
        """
**How this problem links to SDG 13**
- Many air pollutants share sources with **GHG emissions** (transport, industry, power).
- Reducing PM/NO₂ delivers **co-benefits**: cleaner air **and** lower emissions (supports SDG 13.2 integration).
- Trends/Top-5 help track outcomes of **mitigation policies** and identify where action is most needed.
        """
    )


st.markdown("## 💡 Insights we aim to deliver")
st.markdown(
    """
### PM2.5: Fine particles
- These very small particles can reach deep into the lungs and bloodstream.  
- High PM2.5 means higher risks of heart disease, stroke, and premature death.  
- The dashboard shows which regions are above the WHO safe limit (**5 µg/m³**) and whether levels are going up or down over time.  
- Top 5 rankings highlight the countries with the cleanest and dirtiest air.  

### PM10: Coarse particles
- Larger particles that irritate the airways and worsen asthma and bronchitis.  
- Often linked to dust, construction, and industrial activity.  
- The dashboard helps compare regions where PM10 is consistently high, and where policies may be keeping it low.  
- Looking at trends can also show if countries are struggling with seasonal dust or industrial growth.  

### NO₂: Nitrogen Dioxide
- A gas mainly from cars, trucks, and burning fossil fuels.  
- Short-term exposure makes it harder to breathe, especially for children and people with asthma.  
- The dashboard shows where NO₂ levels are above the WHO safe limit (**10 µg/m³**) and how they change over time.  
- Declining trends may suggest cleaner transport or energy policies are working.  

### Cross-cutting insights
- **% Exceeding WHO:** shows how widespread unsafe air is in each region.  
- **Best/Worst performers:** point to countries that can act as role models or where urgent action is needed.  
- **Country table (downloadable):** provides a detailed dataset for further analysis and policy discussions.  
"""
)