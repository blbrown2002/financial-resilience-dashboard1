import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config FIRST
st.set_page_config(page_title="Financial Resilience Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("resilience_scores.csv")  # Make sure this file is in your repo

df = load_data()

# App title and description
st.title("💸 Financial Resilience Dashboard")
st.markdown("""
Use this dashboard to explore which U.S. states are most financially resilient — 
based on median income, unemployment rate, and cost of living.
""")

# Dropdown for state selection
selected_state = st.selectbox("Select a State", df["State"].sort_values())
state_score = df[df["State"] == selected_state]["Resilience_Score"].values[0]
st.metric(label=f"{selected_state} Resilience Score", value=round(state_score, 3))

# Bar chart comparing all states
st.subheader("📊 State Comparison")
fig = px.bar(
    df.sort_values("Resilience_Score", ascending=False),
    x="State",
    y="Resilience_Score",
    title="Financial Resilience by State",
    labels={"Resilience_Score": "Resilience Score"},
    height=500
)
st.plotly_chart(fig, use_container_width=True)
