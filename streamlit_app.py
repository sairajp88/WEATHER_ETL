import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv(dotenv_path="./config/.env")

# --- Streamlit page config ---
st.set_page_config(
    page_title="🌤️ Real-Time Weather Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌦️ Real-Time Weather Dashboard")
st.markdown("🚀 *Visualizing live weather data stored in Snowflake*")

# --- SQLAlchemy engine setup for Snowflake ---
engine = create_engine(URL(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
))

# --- Load weather data ---
@st.cache_data(ttl=300)
def load_weather_data():
    query = "SELECT * FROM WEATHER_DATA ORDER BY TIMESTAMP_UTC DESC LIMIT 1000"
    df = pd.read_sql(text(query), engine)
    df.columns = df.columns.str.upper()  # Normalize columns to uppercase
    return df

df = load_weather_data()

# --- Data Checks ---
if "TIMESTAMP_UTC" not in df.columns:
    st.error("Column 'TIMESTAMP_UTC' missing. Please check Snowflake schema.")
    st.stop()
else:
    df["TIMESTAMP_UTC"] = pd.to_datetime(df["TIMESTAMP_UTC"])

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Weather Data")

cities = df["CITY"].dropna().unique().tolist()
selected_cities = st.sidebar.multiselect("🏙️ Cities", options=cities, default=cities)

conditions = df["WEATHER_MAIN"].dropna().unique().tolist()
selected_conditions = st.sidebar.multiselect("⛅ Conditions", options=conditions, default=conditions)

min_date = df["TIMESTAMP_UTC"].min().date()
max_date = df["TIMESTAMP_UTC"].max().date()
selected_range = st.sidebar.date_input("📅 Date Range", [min_date, max_date])

# --- Apply Filters ---
filtered_df = df[
    (df["CITY"].isin(selected_cities)) &
    (df["WEATHER_MAIN"].isin(selected_conditions)) &
    (df["TIMESTAMP_UTC"].dt.date >= selected_range[0]) &
    (df["TIMESTAMP_UTC"].dt.date <= selected_range[1])
]

if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters.")
    st.stop()

# --- KPIs ---
latest = filtered_df.sort_values("TIMESTAMP_UTC", ascending=False).iloc[0]
col1, col2, col3 = st.columns(3)
col1.metric("🌡️ Temperature (°C)", f"{latest['TEMPERATURE_C']} °C")
col2.metric("💧 Humidity (%)", f"{latest['HUMIDITY']} %")
col3.metric("🌬️ Wind Speed (m/s)", f"{latest['WIND_SPEED']}")

st.markdown("### 📈 Weather Trends Over Time")

# --- Line Charts ---
chart_cols = st.columns(3)

with chart_cols[0]:
    st.subheader("🌡️ Temperature")
    temp_pivot = filtered_df.pivot_table(index="TIMESTAMP_UTC", columns="CITY", values="TEMPERATURE_C")
    st.line_chart(temp_pivot)

with chart_cols[1]:
    st.subheader("💧 Humidity")
    hum_pivot = filtered_df.pivot_table(index="TIMESTAMP_UTC", columns="CITY", values="HUMIDITY")
    st.line_chart(hum_pivot)

with chart_cols[2]:
    st.subheader("🌬️ Wind Speed")
    wind_pivot = filtered_df.pivot_table(index="TIMESTAMP_UTC", columns="CITY", values="WIND_SPEED")
    st.line_chart(wind_pivot)

# --- Weather Type Distribution ---
st.markdown("### ☁️ Weather Conditions Breakdown")
col_pie, col_table = st.columns([1, 1])
with col_pie:
    weather_counts = filtered_df["WEATHER_MAIN"].value_counts()
    st.bar_chart(weather_counts)

with col_table:
    st.dataframe(weather_counts.reset_index().rename(columns={"index": "Condition", "WEATHER_MAIN": "Count"}))

# --- Raw Data Toggle ---
with st.expander("📊 Show Raw Data"):
    st.dataframe(filtered_df)
