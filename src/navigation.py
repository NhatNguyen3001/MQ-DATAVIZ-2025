import streamlit as st

def navigation_bar():
    welcome = st.Page("page_welcome.py", title="Welcome", icon="👋")
    dashboard = st.Page("page_dashboard.py", title="Dashboard", icon="📊")
    credits = st.Page("page_credits.py", title="Credits", icon="👥")
    problem_statement = st.Page("page_problem_statement.py", title="Problem Statement", icon="🎯")
    
    pg = st.navigation([welcome, problem_statement, dashboard, credits])
    
    pg.run()