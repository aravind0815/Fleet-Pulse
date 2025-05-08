# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from utils.db import get_connection
# from utils.styles import set_custom_theme
# from io import BytesIO

# st.set_page_config(page_title="🚛 Fleet Summary Report", layout="wide")
# set_custom_theme()

# st.title("📄 Advanced Fleet Health Report")
# st.markdown("""
# This intelligent report summarizes the operational health of the entire fleet,
# highlights anomalies, ranks truck risk, and provides exportable and printable insights
# backed by machine learning predictions.
# """)

# # --- Date Filter ---
# with st.sidebar:
#     st.markdown("### 🗓️ Select Date Range")
#     start_date = st.date_input("Start Date", pd.Timestamp.now().normalize() - pd.Timedelta(days=7))
#     end_date = st.date_input("End Date", pd.Timestamp.now().normalize())
#     if start_date > end_date:
#         st.error("❌ End date must be after start date")
#         st.stop()

# start_ts = pd.to_datetime(start_date)
# end_ts = pd.to_datetime(end_date + pd.Timedelta(days=1))

# query = f"""
#     SELECT truck_id, timestamp::timestamp, speed, temperature, breakdown_risk, latitude, longitude
#     FROM truck_breakdown_logs
#     WHERE timestamp BETWEEN '{start_ts}' AND '{end_ts}';
# """

# with get_connection() as conn:
#     df = pd.read_sql(query, conn)

# if df.empty:
#     st.warning("No data available in the selected range.")
#     st.stop()

# # --- Metrics ---
# st.subheader("📊 Key Fleet Metrics")
# total_trucks = df['truck_id'].nunique()
# high_risk_count = df[df['breakdown_risk'] >= 0.7]['truck_id'].nunique()
# avg_risk = df['breakdown_risk'].mean()

# col1, col2, col3 = st.columns(3)
# col1.metric("Total Active Trucks", total_trucks)
# col2.metric("Trucks with High Risk", high_risk_count)
# col3.metric("Fleet Avg Breakdown Risk", f"{avg_risk:.2f}")

# # --- Risk Timeline ---
# st.subheader("📈 Average Breakdown Risk Over Time")
# df['timestamp'] = pd.to_datetime(df['timestamp'])
# df['time_slot'] = df['timestamp'].dt.floor('H')
# timeline = df.groupby('time_slot')['breakdown_risk'].mean().reset_index()
# fig1, ax1 = plt.subplots(figsize=(10, 4))
# ax1.plot(timeline['time_slot'], timeline['breakdown_risk'], marker='o', color='#e74c3c')
# ax1.set_title("Average Breakdown Risk (Hourly)")
# ax1.set_xlabel("Time")
# ax1.set_ylabel("Risk")
# ax1.grid(True)
# st.pyplot(fig1)

# # --- Heatmap Risk Distribution ---
# st.subheader("🧯 Risk Distribution Heatmap")
# heatmap_data = df.copy()
# heatmap_data['hour'] = heatmap_data['timestamp'].dt.hour
# heatmap_data['day'] = heatmap_data['timestamp'].dt.date
# pivot = heatmap_data.pivot_table(index='hour', columns='day', values='breakdown_risk', aggfunc='mean')
# st.dataframe(pivot.style.background_gradient(cmap='OrRd', axis=0))

# # --- High Risk Snapshot ---
# st.subheader("🚨 Top 10 High Risk Events")
# high_risk_events = df[df['breakdown_risk'] >= 0.7].sort_values(by='breakdown_risk', ascending=False).head(10)
# st.dataframe(high_risk_events, use_container_width=True)

# # --- Export CSV ---
# st.subheader("📥 Export Report")
# csv = df.to_csv(index=False).encode('utf-8')
# st.download_button("📤 Download Full CSV", csv, file_name="fleet_summary_report.csv", mime="text/csv")

# # --- Printable Summary ---
# st.subheader("🧾 Summary Block")
# st.markdown(f"""
# - **Date Range:** {start_ts.date()} to {end_ts.date()}
# - **Active Trucks:** {total_trucks}
# - **Critical Events (Risk >= 0.7):** {high_risk_count}
# - **Average Risk Fleetwide:** {avg_risk:.2f}
# - **Top Risk Truck:** {df.groupby('truck_id')['breakdown_risk'].max().idxmax()} ({df.groupby('truck_id')['breakdown_risk'].max().max():.2f})
# """)

# st.toast("✅ Fleet report generated successfully.")


import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.db import get_connection
from utils.styles import set_custom_theme

# Setup
st.set_page_config(page_title="📄 Fleet Risk Report", layout="wide")
set_custom_theme()
st.title("📄 Fleet Health & Risk Intelligence Report")

# Sidebar filters
with st.sidebar:
    st.markdown("### 🕒 Filter by Date")
    start_date = st.date_input("Start Date", pd.Timestamp.now() - pd.Timedelta(days=7))
    end_date = st.date_input("End Date", pd.Timestamp.now())
    if start_date > end_date:
        st.error("Start date must be before end date.")
        st.stop()

# Convert to timestamp
start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date + pd.Timedelta(days=1))

# SQL Query
query = f"""
    SELECT timestamp::timestamp, truck_id, speed, temperature, breakdown_risk AS risk,
           latitude, longitude
    FROM truck_breakdown_logs
    WHERE timestamp BETWEEN '{start_ts}' AND '{end_ts}' AND breakdown_risk >= 0.7
    ORDER BY risk DESC
    LIMIT 100;
"""

with get_connection() as conn:
    df = pd.read_sql(query, conn)

if df.empty:
    st.warning("No high-risk breakdowns found for the selected period.")
    st.stop()

# Clean and format
df.dropna(subset=["latitude", "longitude", "truck_id"], inplace=True)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["truck_id"] = df["truck_id"].astype(str)

# KPIs
st.subheader("🔢 Summary")
col1, col2 = st.columns(2)
col1.metric("Total High-Risk Events", len(df))
col2.metric("Avg Risk Score", f"{df['risk'].mean():.2f}")

# High-Risk Table
st.subheader("🔥 Top Breakdown Events")
st.dataframe(df[["timestamp", "truck_id", "speed", "temperature", "risk"]].head(10), use_container_width=True)

# Risk Map
st.subheader("🗺️ High-Risk Locations Heatmap")
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_weight="risk",
    radiusPixels=60,
)

view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=4,
    pitch=30,
)

st.pydeck_chart(pdk.Deck(layers=[heatmap_layer], initial_view_state=view_state))

# Download CSV
st.subheader("⬇️ Download Report")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="fleet_risk_report.csv", mime="text/csv")

st.success("📋 Report generated successfully!")
