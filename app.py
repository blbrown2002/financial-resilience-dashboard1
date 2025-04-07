import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config FIRST
st.set_page_config(page_title="Financial Resilience Dashboard", layout="wide")

# Load raw data (no caching so sliders work)
def load_data():
    return pd.read_csv("resilience_scores_full.csv")

df = load_data()

# ---------------------------------------------
# 🎛️ SIDEBAR: Adjustable Weights
# ---------------------------------------------
st.sidebar.header("⚖️ Adjust Score Weights")

w_income = st.sidebar.slider("Weight: Income", 0.0, 1.0, 0.4, 0.05)
w_unemployment = st.sidebar.slider("Weight: Unemployment", 0.0, 1.0, 0.3, 0.05)
w_cost = st.sidebar.slider("Weight: Cost of Living", 0.0, 1.0, 0.3, 0.05)

# Normalize weights so they sum to 1
total = w_income + w_unemployment + w_cost
w_income, w_unemployment, w_cost = (
    w_income / total,
    w_unemployment / total,
    w_cost / total,
)

st.sidebar.markdown("**Normalized Weights**")
st.sidebar.write(f"- Income: `{w_income:.2f}`")
st.sidebar.write(f"- Unemployment: `{w_unemployment:.2f}`")
st.sidebar.write(f"- Cost: `{w_cost:.2f}`")

# ---------------------------------------------
# 🧮 Recalculate Resilience Score (Live)
# ---------------------------------------------
df["Resilience_Score"] = (
    w_income * df["Income_Norm"] +
    w_unemployment * (1 - df["Unemployment_Norm"]) +
    w_cost * (1 - df["Cost_Norm"])
).round(3)

# ---------------------------------------------
# 🧾 App Header
# ---------------------------------------------
st.title("💸 Financial Resilience Dashboard")
st.markdown("""
Use this dashboard to explore which U.S. states are most financially resilient — 
based on median income, unemployment rate, and cost of living.
""")

# ---------------------------------------------
# 🔍 State Selector
# ---------------------------------------------
selected_state = st.selectbox("Select a State", df["State"].sort_values())
state_score = df[df["State"] == selected_state]["Resilience_Score"].values[0]
st.metric(label=f"{selected_state} Resilience Score", value=round(state_score, 3))

# ---------------------------------------------
# 📊 Bar Chart
# ---------------------------------------------
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

# ---------------------------------------------
# 🗺️ Choropleth Map
# ---------------------------------------------
st.subheader("🗺️ U.S. Resilience Map")

# Map state names to abbreviations
state_abbr = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
df["State_Abbr"] = df["State"].map(state_abbr)

fig_map = px.choropleth(
    df,
    locations="State_Abbr",
    locationmode="USA-states",
    color="Resilience_Score",
    scope="usa",
    color_continuous_scale="Viridis",
    labels={"Resilience_Score": "Resilience Score"},
    title="Financial Resilience Score by State"
)
st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------------------------
# 📊 Score Breakdown Table
# ---------------------------------------------
st.subheader("🧮 Resilience Score Breakdown")

breakdown_df = df[[
    "State",
    "Income_Norm",
    "Unemployment_Norm",
    "Cost_Norm",
    "Resilience_Score"
]].copy()

breakdown_df.columns = [
    "State",
    "Income (Normalized)",
    "Unemployment (Normalized)",
    "Cost of Living (Normalized)",
    "Resilience Score"
]

st.dataframe(breakdown_df.round(3), use_container_width=True)

# ---------------------------------------------
# 🏆 Top & Bottom Resilience Rankings
# ---------------------------------------------
st.subheader("🏆 Top 5 Most Resilient States")
top5_df = df.sort_values("Resilience_Score", ascending=False).head(5)[["State", "Resilience_Score"]]
st.dataframe(top5_df, use_container_width=True)

st.subheader("⚠️ Bottom 5 Least Resilient States")
bottom5_df = df.sort_values("Resilience_Score", ascending=True).head(5)[["State", "Resilience_Score"]]
st.dataframe(bottom5_df, use_container_width=True)
