import streamlit as st
import pandas as pd
import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="weather_data",
    user="postgres",
    password="postgres123"
)

# Fetch data
@st.cache_data
def load_data():
    query = "SELECT * FROM weather.weather_reports ORDER BY timestamp DESC"
    return pd.read_sql(query, conn)

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
city_filter = st.sidebar.multiselect("City", options=df['city'].unique(), default=df['city'].unique())

# Apply filters
filtered_df = df[df['city'].isin(city_filter)]

# Dashboard
st.title("🌤️ Multi-City Weather Dashboard")
st.markdown("Latest weather data fetched hourly via Airflow")

# Display Table
st.dataframe(filtered_df)

# Charts
st.subheader("📈 Temperature Trends")
chart_data = filtered_df.sort_values("timestamp")
st.line_chart(chart_data.pivot(index="timestamp", columns="city", values="temperature"))

conn.close()
