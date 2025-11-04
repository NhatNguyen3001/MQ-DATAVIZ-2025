# MQ Data Visualization Project 2025 - Air Quality Interactive Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mq-dataviz-2025.streamlit.app/)

A comprehensive data visualization dashboard built with Streamlit to analyze and present insights on air quality data. This interactive application helps users explore air pollution patterns, trends, and their impacts on public health and the environment.

🔗 **Live Demo**: [https://mq-dataviz-2025.streamlit.app/](https://mq-dataviz-2025.streamlit.app/)

## 📋 Project Overview

Air quality is a critical environmental and public health concern affecting millions of people worldwide. Poor air quality contributes to respiratory diseases, cardiovascular problems, and has significant economic impacts. This project provides an interactive platform to:

- Visualize air quality metrics and pollutant concentrations
- Identify temporal and spatial patterns in air pollution
- Analyze the relationship between different pollutants
- Support data-driven decision-making for environmental policy

### Background

Air pollution is caused by various sources including industrial emissions, vehicle exhaust, and natural phenomena. Key pollutants monitored include:
- **PM2.5 & PM10**: Particulate matter that can penetrate deep into lungs
- **NO2**: Nitrogen dioxide from combustion processes

Understanding these pollutants' behavior and trends is crucial for developing effective air quality management strategies.

## 🎯 Problem Statement

Despite the availability of air quality monitoring data, making this information accessible and actionable remains a challenge. This project addresses:

1. **Data Complexity**: Raw air quality data is difficult for non-experts to interpret
2. **Temporal Patterns**: Understanding how air quality changes over time requires sophisticated visualization
3. **Public Awareness**: Need for accessible tools to inform communities about air quality risks
4. **Decision Support**: Policymakers require clear insights to develop targeted interventions

Our dashboard transforms complex air quality datasets into intuitive, interactive visualizations that enable:
- Quick assessment of air quality conditions
- Identification of pollution hotspots and trends
- Evidence-based environmental health recommendations

## 🚀 Features

- **Interactive Dashboard**: Dynamic visualizations with filtering and exploration capabilities
- **Time Series Analysis**: Track air quality trends over different time periods
- **Pollutant Correlations**: Explore relationships between different air pollutants
- **Statistical Insights**: In-depth analysis with descriptive statistics
- **Responsive Design**: User-friendly interface with intuitive navigation

## 📁 Project Structure

```
MQ-DATAVIZ-2025/
│
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
│
├── src/                           # Source code directory
│   ├── app.py                     # Main application entry point
│   ├── navigation.py              # Page navigation logic
│   ├── utils.py                   # Utility functions
│   ├── page_welcome.py            # Welcome/landing page
│   ├── page_problem_statement.py  # Problem definition page
│   ├── page_dashboard.py          # Main dashboard page
│   └── page_credits.py            # Credits and acknowledgments
│
├── data/
│   └── processed.csv              # Processed air quality dataset
│
├── experiments/
│   ├── data_processing.ipynb      # Data cleaning and processing
│   ├── EDA.ipynb                  # Exploratory data analysis
│   └── handling_nulls_documentation.md
│
└── img/                           # Image assets
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/NhatNguyen3001/MQ-DATAVIZ-2025.git
   cd MQ-DATAVIZ-2025
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage

### Run Locally

```bash
streamlit run src/app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Access Online

Visit the live deployment: [https://mq-dataviz-2025.streamlit.app/](https://mq-dataviz-2025.streamlit.app/)

## 📊 Data

The project uses a processed air quality dataset located in `data/processed.csv`. 

**Data Processing Steps:**
- See `experiments/data_processing.ipynb` for data cleaning pipeline
- See `experiments/handling_nulls_documentation.md` for null value handling strategies
- See `experiments/EDA.ipynb` for exploratory data analysis

**Dataset Features:**
- Multiple air quality pollutants (PM2.5, PM10, NO2)
- Temporal information (dates, times)
- Location/station identifiers

## 🧪 Experiments

The `experiments/` folder contains Jupyter notebooks documenting:
- Data preprocessing and cleaning
- Exploratory data analysis (EDA)
- Feature engineering
- Statistical analysis
- Null value handling strategies

## 📦 Dependencies

Key dependencies include:
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Altair** - data visualization

See `requirements.txt` for complete list.

---
**Note**: This project was created as a submission for the **MQ DataViz Competition 2025** at Macquarie University.