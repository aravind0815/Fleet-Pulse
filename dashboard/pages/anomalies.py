# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from utils.db import get_connection
# from utils.styles import set_custom_theme

# st.set_page_config(page_title="📈 Anomaly Detection", layout="wide")
# set_custom_theme()
# st.title("📈 Anomaly Detection in Truck Data")
# st.markdown(
#     "This page visualizes **unusual spikes or drops** in temperature and speed for each truck. "
#     "We use **Z-score-based detection** to flag outliers in the last 24 hours of data."
# )

# # 🔌 Connect to DB
# conn = get_connection()

# # 🧠 Fetch Data
# query = """
#     SELECT truck_id, timestamp::timestamp AS ts, speed, temperature, breakdown_risk
#     FROM truck_breakdown_logs
#     WHERE timestamp::timestamp >= NOW() - INTERVAL '1 day'
#     ORDER BY truck_id, ts
# """
# df = pd.read_sql(query, conn)

# if df.empty:
#     st.warning("No truck data available for anomaly detection in the last 24 hours.")
#     st.stop()

# # 📌 Truck selector
# truck_ids = df["truck_id"].unique()
# selected_truck = st.selectbox("Select a truck to view anomalies", truck_ids)

# truck_df = df[df["truck_id"] == selected_truck].copy()

# if len(truck_df) < 10:
#     st.info("Not enough data for this truck to detect anomalies.")
#     st.stop()

# # 🧪 Z-score based anomaly detection
# for col in ["temperature", "speed"]:
#     truck_df[f"{col}_z"] = (truck_df[col] - truck_df[col].mean()) / truck_df[col].std()
#     truck_df[f"{col}_anomaly"] = truck_df[f"{col}_z"].abs() > 2.5

# # 📊 Temperature Trend with Anomalies
# st.subheader("🌡️ Temperature Trend (Last 24h)")

# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(truck_df["ts"], truck_df["temperature"], label="Temperature", color="orange")
# anomalies = truck_df[truck_df["temperature_anomaly"]]
# ax.scatter(anomalies["ts"], anomalies["temperature"], color="red", label="Anomaly", zorder=5)
# ax.set_ylabel("Temperature (°C)")
# ax.set_xlabel("Time")
# ax.legend()
# st.pyplot(fig)

# # 📊 Speed Trend with Anomalies
# st.subheader("🚚 Speed Trend (Last 24h)")

# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(truck_df["ts"], truck_df["speed"], label="Speed", color="blue")
# anomalies = truck_df[truck_df["speed_anomaly"]]
# ax.scatter(anomalies["ts"], anomalies["speed"], color="red", label="Anomaly", zorder=5)
# ax.set_ylabel("Speed (km/h)")
# ax.set_xlabel("Time")
# ax.legend()
# st.pyplot(fig)

# # 🧾 Tabular view of anomalies
# st.subheader("📋 View Anomaly Data")
# display_df = truck_df[
#     (truck_df["temperature_anomaly"]) | (truck_df["speed_anomaly"])
# ][["ts", "speed", "temperature", "breakdown_risk"]]

# if display_df.empty:
#     st.info("No strong anomalies detected for this truck in the last 24 hours.")
# else:
#     st.dataframe(display_df.sort_values("ts", ascending=False), use_container_width=True)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import get_connection
from utils.styles import set_custom_theme

# --- Page Config ---
st.set_page_config(page_title="Fleet Anomaly Trends", layout="wide")

# --- Theme ---
set_custom_theme()

# --- Sidebar Filters ---
with st.sidebar:
    st.markdown("### 🔍 Filters")
    start_date = st.date_input("Start Date", pd.Timestamp.now().normalize() - pd.Timedelta(days=5))
    end_date = st.date_input("End Date", pd.Timestamp.now().normalize())

    if start_date > end_date:
        st.error("End date must be after start date")

    with get_connection() as conn:
        truck_options = pd.read_sql("SELECT DISTINCT truck_id FROM truck_breakdown_logs;", conn)
        truck_ids = truck_options["truck_id"].tolist()

    selected_truck = st.selectbox("Select Truck", ["All"] + truck_ids)

# --- Filter Clause ---
filter_clause = f"timestamp BETWEEN '{start_date}' AND '{end_date}'"
if selected_truck != "All":
    filter_clause += f" AND truck_id = '{selected_truck}'"

st.markdown("## 📈 Anomaly Detection in Truck Data")
st.markdown("This page highlights unusual patterns in truck temperature and speed data over time. Spikes and dips may indicate maintenance issues or risky driving behavior.")

# --- Anomaly Data ---
anomaly_query = f"""
    SELECT truck_id, timestamp::timestamp, speed, temperature, breakdown_risk
    FROM truck_breakdown_logs
    WHERE {filter_clause}
    ORDER BY truck_id, timestamp
    LIMIT 2000;
"""
with get_connection() as conn:
    df = pd.read_sql(anomaly_query, conn)

if df.empty:
    st.warning("No data found for the selected filters.")
else:
    st.success(f"Loaded {len(df)} records.")

    # --- Line Chart: Speed & Temp by Time ---
    st.markdown("### 📊 Speed & Temperature Over Time")
    selected_chart_truck = st.selectbox("Select Truck for Trend Graphs", sorted(df['truck_id'].unique()))
    filtered = df[df['truck_id'] == selected_chart_truck]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered['timestamp'], filtered['speed'], label="Speed (km/h)", color='#3498db')
    ax.set_ylabel("Speed", color='#3498db')
    ax2 = ax.twinx()
    ax2.plot(filtered['timestamp'], filtered['temperature'], label="Temperature (°C)", color='#e67e22')
    ax2.set_ylabel("Temperature", color='#e67e22')
    ax.set_title(f"Truck {selected_chart_truck} - Speed & Temperature")
    fig.autofmt_xdate()
    st.pyplot(fig)

    # --- Breakdown Risk ---
    st.markdown("### 🔥 Breakdown Risk Timeline")
    fig2, ax3 = plt.subplots(figsize=(10, 3))
    ax3.plot(filtered['timestamp'], filtered['breakdown_risk'], color='#e74c3c', marker='o')
    ax3.axhline(0.7, linestyle='--', color='orange', label="High Risk Threshold")
    ax3.set_title(f"Breakdown Risk for Truck {selected_chart_truck}")
    ax3.set_ylabel("Risk")
    ax3.set_xlabel("Timestamp")
    fig2.autofmt_xdate()
    st.pyplot(fig2)

    st.markdown("---")
    st.markdown("#### 📝 Notes:")
    st.markdown("- A spike in risk alongside unusual temperature/speed could signal a pending breakdown.")
    st.markdown("- Use this trend to correlate risk behavior with environmental or driver factors.")

st.toast("Anomaly data updated based on filters.")


