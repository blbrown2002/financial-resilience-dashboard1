import streamlit as st
import pandas as pd
import plotly.express as px

# Load the processed data
@st.cache_data
def load_data():
    return pd.read_csv("resilience_scores.csv")  # Save your merged_df to this name

df = load_data()

st.set_page_config(page_title="Financial Resilience Dashboard", layout="wide")

# Title and intro
st.title("💸 Financial Resilience Dashboard")
st.markdown("""
Use this tool to explore which U.S. states are most financially resilient — based on income, unemployment, and cost of living data.
""")

# Dropdown for state selection
selected_state = st.selectbox("Select a State", df["State"].sort_values())

# Show resilience score
state_score = df[df["State"] == selected_state]["Resilience_Score"].values[0]
st.metric(label=f"{selected_state} Resilience Score", value=round(state_score, 3))

# Bar chart of all states
st.subheader("📊 State Comparison")
fig = px.bar(df.sort_values("Resilience_Score", ascending=False),
             x="State", y="Resilience_Score",
             title="Financial Resilience by State",
             labels={"Resilience_Score": "Resilience Score"},
             height=500)
st.plotly_chart(fig, use_container_width=True)
