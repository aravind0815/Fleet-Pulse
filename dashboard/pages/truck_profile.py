# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from utils.db import get_connection
# from utils.styles import set_custom_theme

# st.set_page_config(page_title="Truck Profile & Diagnostics", layout="wide")
# set_custom_theme()

# st.title("🚛 Truck Profile Dashboard")
# st.markdown("Gain deep insights into the health, performance, and breakdown risk trends of an individual truck.")

# # --- Sidebar Filters ---
# with st.sidebar:
#     st.markdown("### 🔎 Truck Selection")
#     with get_connection() as conn:
#         truck_ids_df = pd.read_sql("SELECT DISTINCT truck_id FROM truck_breakdown_logs ORDER BY truck_id;", conn)
#         truck_ids = truck_ids_df["truck_id"].astype(str).tolist()
#         selected_truck = st.selectbox("Select Truck", truck_ids)

#     start_date = st.date_input("Start Date", pd.Timestamp.now().normalize() - pd.Timedelta(days=7))
#     end_date = st.date_input("End Date", pd.Timestamp.now().normalize())

# if start_date > end_date:
#     st.error("End date must be after start date")
#     st.stop()

# start_ts = pd.to_datetime(start_date)
# end_ts = pd.to_datetime(end_date + pd.Timedelta(days=1))

# # --- SQL Query ---
# query = f"""
#     SELECT timestamp::timestamp, speed, temperature, breakdown_risk, latitude, longitude
#     FROM truck_breakdown_logs
#     WHERE truck_id = {int(float(selected_truck))}
#       AND timestamp BETWEEN '{start_ts}' AND '{end_ts}'
#     ORDER BY timestamp;
# """

# with get_connection() as conn:
#     df = pd.read_sql(query, conn)

# if df.empty:
#     st.warning("No data found for selected truck and date range.")
#     st.stop()

# # --- Stats ---
# st.subheader("📊 Key Performance Indicators")
# col1, col2, col3 = st.columns(3)
# col1.metric("Avg Speed", f"{df['speed'].mean():.1f} km/h")
# col2.metric("Avg Temperature", f"{df['temperature'].mean():.1f} °C")
# col3.metric("Max Risk", f"{df['breakdown_risk'].max():.2f}")

# # --- Speed/Temp Trend ---
# st.subheader("📈 Speed & Temperature Over Time")
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(df["timestamp"], df["speed"], label="Speed", color="#3498db")
# ax.set_ylabel("Speed (km/h)", color="#3498db")
# ax2 = ax.twinx()
# ax2.plot(df["timestamp"], df["temperature"], label="Temperature", color="#e67e22")
# ax2.set_ylabel("Temp (°C)", color="#e67e22")
# fig.autofmt_xdate()
# st.pyplot(fig)

# # --- Risk Timeline ---
# st.subheader("🔥 Breakdown Risk Timeline")
# fig2, ax3 = plt.subplots(figsize=(10, 3))
# ax3.plot(df["timestamp"], df["breakdown_risk"], color="#e74c3c", marker="o")
# ax3.axhline(0.7, linestyle="--", color="orange", label="Threshold")
# ax3.set_ylabel("Risk")
# ax3.set_xlabel("Time")
# fig2.autofmt_xdate()
# st.pyplot(fig2)

# # --- Risk Daily Average ---
# st.subheader("🧠 Daily Avg Breakdown Risk")
# daily_avg = df.copy()
# daily_avg["date"] = daily_avg["timestamp"].dt.date
# daily_summary = daily_avg.groupby("date")["breakdown_risk"].mean().reset_index()
# fig3, ax4 = plt.subplots()
# ax4.bar(daily_summary["date"], daily_summary["breakdown_risk"], color="#9b59b6")
# ax4.set_ylabel("Avg Risk")
# ax4.set_xlabel("Date")
# st.pyplot(fig3)

# # --- Location Timeline ---
# st.subheader("🛰️ Last Known GPS Location")
# latest = df.dropna(subset=["latitude", "longitude"]).iloc[-1]
# st.markdown(f"**Last Recorded Location:** ({latest['latitude']:.4f}, {latest['longitude']:.4f}) @ {latest['timestamp']}")

# # --- Maintenance Advisory ---
# st.subheader("🧾 Maintenance Suggestion")
# if df['breakdown_risk'].max() >= 0.9:
#     st.error("🚨 Critical risk level detected. Immediate diagnostic check recommended.")
# elif df['breakdown_risk'].mean() > 0.5:
#     st.warning("⚠️ Moderate risk observed over this time period. Consider a checkup.")
# else:
#     st.success("✅ Truck performance is stable. No immediate maintenance action needed.")

# # --- Raw ---
# with st.expander("📄 View Raw Sensor Data"):
#     st.dataframe(df, use_container_width=True)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import get_connection
from utils.styles import set_custom_theme

# Setup
st.set_page_config(page_title="🚛 Truck Profile & Diagnostics", layout="wide")
set_custom_theme()

st.title("🚛 Truck Profile Dashboard")
st.markdown("Gain deep insights into the health, performance, and breakdown risk trends of an individual truck using AI-powered analytics.")

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🔎 Truck Selection")
    with get_connection() as conn:
        truck_ids_df = pd.read_sql("SELECT DISTINCT truck_id FROM truck_breakdown_logs ORDER BY truck_id;", conn)
        truck_ids = truck_ids_df["truck_id"].astype(str).tolist()
        selected_truck = int(float(st.selectbox("Select Truck", truck_ids)))


    st.markdown("---")
    st.markdown("### 📅 Date Range")
    start_date = st.date_input("Start Date", pd.Timestamp.now().normalize() - pd.Timedelta(days=7))
    end_date = st.date_input("End Date", pd.Timestamp.now().normalize())

if start_date > end_date:
    st.error("End date must be after start date")
    st.stop()

start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date + pd.Timedelta(days=1))

# Query truck data
query = f"""
    SELECT timestamp::timestamp, speed, temperature, breakdown_risk, latitude, longitude
    FROM truck_breakdown_logs
    WHERE truck_id = '{selected_truck}'
      AND timestamp BETWEEN '{start_ts}' AND '{end_ts}'
    ORDER BY timestamp;
"""

with get_connection() as conn:
    df = pd.read_sql(query, conn)

if df.empty:
    st.warning("No data found for selected truck and date range.")
    st.stop()

# Key KPIs
st.subheader("📊 Smart Performance Summary")
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Avg Speed", f"{df['speed'].mean():.1f} km/h")
col2.metric("🌡️ Avg Temp", f"{df['temperature'].mean():.1f} °C")
col3.metric("🔥 Max Risk", f"{df['breakdown_risk'].max():.2f}")

# Speed/Temp Timeline
st.subheader("📈 Speed & Temperature Timeline")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df["timestamp"], df["speed"], label="Speed", color="#3498db")
ax.set_ylabel("Speed (km/h)", color="#3498db")
ax2 = ax.twinx()
ax2.plot(df["timestamp"], df["temperature"], label="Temperature", color="#e67e22")
ax2.set_ylabel("Temperature (°C)", color="#e67e22")
fig.autofmt_xdate()
st.pyplot(fig)

# Risk Timeline
st.subheader("🧠 Breakdown Risk Over Time")
fig2, ax3 = plt.subplots(figsize=(12, 3))
ax3.plot(df["timestamp"], df["breakdown_risk"], color="#e74c3c", marker="o")
ax3.axhline(0.7, linestyle="--", color="orange", label="Risk Threshold")
ax3.set_ylabel("Risk Score")
ax3.set_xlabel("Timestamp")
fig2.autofmt_xdate()
st.pyplot(fig2)

# Risk Daily Averages
st.subheader("📅 Daily Risk Analysis")
df["date"] = pd.to_datetime(df["timestamp"]).dt.date
daily_summary = df.groupby("date")["breakdown_risk"].mean().reset_index()
fig3, ax4 = plt.subplots()
ax4.bar(daily_summary["date"], daily_summary["breakdown_risk"], color="#9b59b6")
ax4.set_ylabel("Average Risk")
ax4.set_xlabel("Date")
st.pyplot(fig3)

# Last GPS Location
st.subheader("🛰️ Last Known Location")
latest = df.dropna(subset=["latitude", "longitude"]).iloc[-1]
st.markdown(f"**Last Location:** {latest['latitude']:.4f}, {latest['longitude']:.4f} at {latest['timestamp']}")

# AI-based Advisory
st.subheader("🔧 AI Maintenance Suggestion")
if df['breakdown_risk'].max() >= 0.9:
    st.error("🚨 Immediate diagnostic required! Critical breakdown risk detected.")
elif df['breakdown_risk'].mean() > 0.5:
    st.warning("⚠️ Moderate risk observed. Schedule a preventive check.")
else:
    st.success("✅ No urgent action needed. Truck performance is stable.")

# Show Raw Data
with st.expander("📄 Show Raw Data"):
    st.dataframe(df, use_container_width=True)

# Export Option
st.download_button(
    "⬇️ Download CSV Report",
    df.to_csv(index=False).encode("utf-8"),
    file_name=f"truck_{selected_truck}_profile_report.csv",
    mime="text/csv"
)
