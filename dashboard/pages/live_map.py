import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.db import get_connection
from utils.styles import set_custom_theme

st.set_page_config(page_title="Live Truck Map", layout="wide")
set_custom_theme()

st.title("🛰️ Current Truck Positions")

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🔎 Filters")
    start_date = st.date_input("Start Time", pd.Timestamp.now().normalize() - pd.Timedelta(days=1))
    end_date = st.date_input("End Time", pd.Timestamp.now().normalize())

    with get_connection() as conn:
        truck_ids_query = "SELECT DISTINCT truck_id FROM truck_breakdown_logs ORDER BY truck_id;"
        truck_ids_df = pd.read_sql(truck_ids_query, conn)
        truck_ids = truck_ids_df["truck_id"].astype(str).tolist()
        selected_truck = st.selectbox("Truck ID", ["All"] + truck_ids)

# SQL Query
start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date + pd.Timedelta(days=1))
filter_clause = f"timestamp BETWEEN '{start_ts}' AND '{end_ts}' AND latitude IS NOT NULL AND longitude IS NOT NULL"
if selected_truck != "All":
    filter_clause += f" AND truck_id = {int(float(selected_truck))}"

query = f"""
    SELECT truck_id, timestamp, latitude, longitude, breakdown_risk
    FROM truck_breakdown_logs
    WHERE {filter_clause} AND breakdown_risk IS NOT NULL
    ORDER BY timestamp DESC
    LIMIT 500;
"""

with get_connection() as conn:
    df = pd.read_sql(query, conn)

if df.empty:
    st.warning("No data available for selected filters.")
else:
    df = df.dropna(subset=["latitude", "longitude"])
    df = df.sort_values("timestamp", ascending=False).drop_duplicates(subset=["truck_id"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["tooltip"] = df.apply(lambda row: f"Truck: {row['truck_id']}<br>Risk: {row['breakdown_risk']:.2f}<br>Time: {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}", axis=1)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[longitude, latitude]",
        get_color="[0, 255, 0, 160]",
        get_radius=40000,
        pickable=True,
        tooltip=True
    )

    view_state = pdk.ViewState(latitude=39.5, longitude=-98.35, zoom=3.5)

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v11',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"html": "{tooltip}", "style": {"color": "white"}}
    ))

    with st.expander("📄 View Raw Data"):
        st.dataframe(df, use_container_width=True)
