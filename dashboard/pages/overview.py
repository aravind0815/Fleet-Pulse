# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from utils.db import get_connection
# from utils.styles import set_custom_theme

# # Page setup
# st.set_page_config(page_title="Fleet Overview", layout="wide")
# set_custom_theme()

# # Smart default filter values
# DEFAULT_START = pd.to_datetime("2025-05-06 18:56:53")
# DEFAULT_END = pd.to_datetime("2025-05-06 19:02:16")

# # --- Sidebar ---
# with st.sidebar:
#     st.markdown("## 🔍 Filters")
#     start_date = st.date_input("Start Date", DEFAULT_START.date())
#     end_date = st.date_input("End Date", DEFAULT_END.date())
#     if start_date > end_date:
#         st.error("❌ End date must be after start date.")
#         st.stop()

# # Convert to timestamp for filtering
# start_ts = pd.to_datetime(start_date)
# end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1)  # include full end day

# st.markdown("## 📊 Fleet Overview")

# # --- Truck filter and data ---
# with get_connection() as conn:
#     truck_options = pd.read_sql("SELECT DISTINCT truck_id FROM truck_breakdown_logs;", conn)
#     all_trucks = ["All"] + sorted(truck_options["truck_id"].astype(str).tolist())

# selected_truck = st.sidebar.selectbox("Select Truck", all_trucks)

# # --- Filter SQL clause ---
# filter_clause = f"timestamp >= '{start_ts}' AND timestamp < '{end_ts}'"
# if selected_truck != "All":
#     filter_clause += f" AND truck_id = '{selected_truck}'"

# st.toast("✅ Data refreshed with selected filters.")
# st.code(f"-- Filter clause:\n{filter_clause}", language="sql")

# # --- Summary Stats ---
# summary_query = f"""
#     SELECT 
#         COUNT(DISTINCT truck_id) AS total_trucks,
#         COUNT(*) FILTER (WHERE breakdown_risk >= 0.7) AS high_risk,
#         MAX(breakdown_risk) AS max_risk
#     FROM truck_breakdown_logs
#     WHERE {filter_clause};
# """
# with get_connection() as conn:
#     summary = pd.read_sql(summary_query, conn)

# if summary.empty:
#     st.warning("No data found for the selected filters.")
#     st.stop()

# col1, col2, col3 = st.columns(3)
# col1.metric("🚛 Total Trucks", int(summary['total_trucks'][0]))
# col2.metric("⚠️ Active Breakdowns", int(summary['high_risk'][0]))
# max_risk = summary['max_risk'][0]
# col3.metric("🔥 Max Risk", f"{max_risk:.2f}" if max_risk is not None else "N/A")

# st.markdown("---")

# # --- Trend Chart ---
# st.subheader("📈 Breakdown Risk Trend (Hourly)")
# trend_query = f"""
#     SELECT 
#         DATE_TRUNC('minute', timestamp::timestamp) AS slot,
#         AVG(breakdown_risk) AS avg_risk
#     FROM truck_breakdown_logs
#     WHERE {filter_clause}
#     GROUP BY slot
#     ORDER BY slot;
# """
# with get_connection() as conn:
#     trend_data = pd.read_sql(trend_query, conn)

# if not trend_data.empty:
#     fig, ax = plt.subplots()
#     ax.plot(trend_data["slot"], trend_data["avg_risk"], marker='o', color='#e74c3c')
#     ax.set_title("Avg Breakdown Risk Over Time")
#     ax.set_ylabel("Avg Risk")
#     ax.set_xlabel("Time")
#     plt.xticks(rotation=45)
#     st.pyplot(fig)
# else:
#     st.info("No trend data available.")

# # --- Risk Pie Chart ---
# st.subheader("🧯 Risk Distribution")
# pie_query = f"""
#     SELECT
#         CASE 
#             WHEN breakdown_risk < 0.4 THEN 'Low'
#             WHEN breakdown_risk < 0.7 THEN 'Medium'
#             ELSE 'High'
#         END AS risk_level,
#         COUNT(*) as count
#     FROM truck_breakdown_logs
#     WHERE {filter_clause}
#     GROUP BY risk_level;
# """
# with get_connection() as conn:
#     pie_df = pd.read_sql(pie_query, conn)

# if not pie_df.empty:
#     fig2, ax2 = plt.subplots()
#     ax2.pie(pie_df["count"], labels=pie_df["risk_level"], autopct='%1.1f%%',
#             startangle=140, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
#     ax2.axis("equal")
#     st.pyplot(fig2)
# else:
#     st.info("No risk distribution data for selected filters.")

# # --- Recent Events ---
# st.subheader("⚠️ Recent High-Risk Breakdown Events")
# events_query = f"""
#     SELECT truck_id, speed, temperature, breakdown_risk, timestamp
#     FROM truck_breakdown_logs
#     WHERE breakdown_risk >= 0.7 AND {filter_clause}
#     ORDER BY timestamp DESC
#     LIMIT 10;
# """
# with get_connection() as conn:
#     recent_df = pd.read_sql(events_query, conn)

# def color_risk(val):
#     if val >= 0.9:
#         return 'background-color: #e74c3c; color: white'
#     elif val >= 0.8:
#         return 'background-color: #f39c12; color: black'
#     return ''

# if recent_df.empty:
#     st.info("No recent high-risk breakdowns.")
# else:
#     st.dataframe(recent_df.style.applymap(color_risk, subset=["breakdown_risk"]), use_container_width=True)


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from utils.db import get_connection
# from utils.styles import set_custom_theme

# # Page Setup
# st.set_page_config(page_title="📊 Fleet Overview Dashboard", layout="wide")
# set_custom_theme()
# st.title("📊 FleetPulse - Real-time Risk Intelligence")
# st.markdown("Analyze fleet-wide performance, breakdown trends, and risk distribution across all trucks in the system.")

# # --- Sidebar Filters ---
# with st.sidebar:
#     st.markdown("## 🔍 Filter Options")
#     with get_connection() as conn:
#         truck_ids = pd.read_sql("SELECT DISTINCT truck_id FROM truck_breakdown_logs ORDER BY truck_id;", conn)
#         truck_list = ["All"] + [str(x) for x in truck_ids["truck_id"]]
#     selected_truck = st.selectbox("🚛 Select Truck", truck_list)

#     start_date = st.date_input("📆 Start Date", pd.Timestamp.now().normalize() - pd.Timedelta(days=7))
#     end_date = st.date_input("📆 End Date", pd.Timestamp.now().normalize())

#     if start_date > end_date:
#         st.error("❌ End date must be after start date.")
#         st.stop()

# # Filter Logic
# start_ts = pd.to_datetime(start_date)
# end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1)
# filter_clause = f"timestamp >= '{start_ts}' AND timestamp < '{end_ts}'"
# if selected_truck != "All":
#     filter_clause += f" AND truck_id = {int(float(selected_truck))}"

# # --- Summary KPIs ---
# st.subheader("🔢 Fleet KPIs")
# sql = f"""
#     SELECT 
#         COUNT(DISTINCT truck_id) AS total_trucks,
#         COUNT(*) FILTER (WHERE breakdown_risk >= 0.7) AS high_risk_events,
#         MAX(breakdown_risk) AS peak_risk
#     FROM truck_breakdown_logs
#     WHERE {filter_clause};
# """
# with get_connection() as conn:
#     metrics = pd.read_sql(sql, conn)

# col1, col2, col3 = st.columns(3)
# col1.metric("🚛 Active Trucks", int(metrics['total_trucks'][0]))
# col2.metric("⚠️ High-Risk Events", int(metrics['high_risk_events'][0]))
# col3.metric("🔥 Peak Risk Score", f"{metrics['peak_risk'][0]:.2f}" if metrics['peak_risk'][0] else "N/A")

# # --- Risk Trend Chart ---
# st.subheader("📈 Breakdown Risk Trend")
# trend_query = f"""
#     SELECT 
#         DATE_TRUNC('hour', timestamp::timestamp) AS hour,
#         AVG(breakdown_risk) AS avg_risk
#     FROM truck_breakdown_logs
#     WHERE {filter_clause}
#     GROUP BY hour
#     ORDER BY hour;
# """
# with get_connection() as conn:
#     trend_df = pd.read_sql(trend_query, conn)

# if trend_df.empty:
#     st.info("No trend data found for selected filters.")
# else:
#     fig, ax = plt.subplots(figsize=(10, 4))
#     ax.plot(trend_df['hour'], trend_df['avg_risk'], marker='o', color='#e74c3c')
#     ax.set_ylabel("Avg Breakdown Risk")
#     ax.set_xlabel("Time")
#     fig.autofmt_xdate()
#     st.pyplot(fig)

# # --- Risk Level Pie Chart ---
# st.subheader("🧯 Risk Distribution Across Events")
# pie_query = f"""
#     SELECT
#         CASE 
#             WHEN breakdown_risk < 0.4 THEN 'Low'
#             WHEN breakdown_risk < 0.7 THEN 'Medium'
#             ELSE 'High'
#         END AS risk_level,
#         COUNT(*) AS event_count
#     FROM truck_breakdown_logs
#     WHERE {filter_clause}
#     GROUP BY risk_level;
# """
# with get_connection() as conn:
#     pie_df = pd.read_sql(pie_query, conn)

# if not pie_df.empty:
#     fig2, ax2 = plt.subplots()
#     ax2.pie(pie_df['event_count'], labels=pie_df['risk_level'], autopct='%1.1f%%',
#             startangle=140, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
#     ax2.axis("equal")
#     st.pyplot(fig2)
# else:
#     st.info("No risk classification data.")

# # --- Breakdown Alerts Table ---
# st.subheader("⚠️ Recent High-Risk Breakdowns")
# alert_query = f"""
#     SELECT truck_id, speed, temperature, breakdown_risk, timestamp
#     FROM truck_breakdown_logs
#     WHERE breakdown_risk >= 0.7 AND {filter_clause}
#     ORDER BY timestamp DESC
#     LIMIT 10;
# """
# with get_connection() as conn:
#     alert_df = pd.read_sql(alert_query, conn)

# def highlight_risk(val):
#     if val >= 0.9:
#         return 'background-color: #e74c3c; color: white'
#     elif val >= 0.8:
#         return 'background-color: #f1c40f; color: black'
#     return ''

# if not alert_df.empty:
#     st.dataframe(alert_df.style.applymap(highlight_risk, subset=['breakdown_risk']), use_container_width=True)
# else:
#     st.info("No critical events during this period.")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import get_connection
from utils.styles import set_custom_theme
from datetime import timedelta

# --- Page Setup ---
st.set_page_config(page_title="🚨 Anomaly Detector", layout="wide")
set_custom_theme()
st.title("🚨 Fleet Anomaly Detection Panel")
st.markdown("Analyze deviations in sensor behavior and breakdown risk. This AI-enhanced module flags sudden spikes and unusual operating patterns for preemptive maintenance.")

# --- Sidebar Filters ---
with st.sidebar:
    st.markdown("## 🔍 Filter Parameters")
    start_date = st.date_input("📆 Start Date", pd.Timestamp.now().normalize() - pd.Timedelta(days=5))
    end_date = st.date_input("📆 End Date", pd.Timestamp.now().normalize())
    
    if start_date > end_date:
        st.error("❌ End date must be after start date.")
        st.stop()

    with get_connection() as conn:
        truck_ids = pd.read_sql("SELECT DISTINCT truck_id FROM truck_breakdown_logs ORDER BY truck_id;", conn)
        truck_list = [str(t) for t in truck_ids["truck_id"]]

    selected_truck = st.selectbox("🚛 Truck ID", ["All"] + truck_list)

# --- Filter Clause ---
start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date) + timedelta(days=1)
filter_clause = f"timestamp >= '{start_ts}' AND timestamp < '{end_ts}'"
if selected_truck != "All":
    filter_clause += f" AND truck_id = {int(float(selected_truck))}"

# --- Load Data ---
st.markdown("---")
st.subheader("📥 Loading Data")
query = f"""
    SELECT timestamp::timestamp, truck_id, speed, temperature, breakdown_risk
    FROM truck_breakdown_logs
    WHERE {filter_clause}
    ORDER BY truck_id, timestamp
    LIMIT 3000;
"""

with get_connection() as conn:
    df = pd.read_sql(query, conn)

if df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

st.success(f"Loaded {len(df)} records.")

# --- Anomaly Detection ---
st.markdown("## 📈 Sensor Spike & Breakdown Risk Timeline")
selected_truck_id = st.selectbox("Choose Truck for Analysis", sorted(df['truck_id'].unique()))
truck_df = df[df['truck_id'] == selected_truck_id].copy()
truck_df.set_index("timestamp", inplace=True)

# --- Moving Average for comparison ---
truck_df["risk_ma"] = truck_df["breakdown_risk"].rolling(window=5, min_periods=1).mean()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(truck_df.index, truck_df["breakdown_risk"], label="Breakdown Risk", marker="o", color="#e74c3c")
ax.plot(truck_df.index, truck_df["risk_ma"], label="Moving Avg (5) Risk", linestyle="--", color="#3498db")
ax.axhline(0.7, linestyle='--', color='orange', label="High Risk Threshold")
ax.set_title(f"Breakdown Risk Timeline - Truck {selected_truck_id}")
ax.set_ylabel("Risk")
ax.set_xlabel("Time")
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# --- Speed & Temp Graph ---
st.markdown("### 🧊 Speed and Temperature Trends")
fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.plot(truck_df.index, truck_df["speed"], color='#1abc9c', label="Speed")
ax2.set_ylabel("Speed (km/h)", color='#1abc9c')
ax2b = ax2.twinx()
ax2b.plot(truck_df.index, truck_df["temperature"], color='#e67e22', label="Temperature")
ax2b.set_ylabel("Temperature (°C)", color='#e67e22')
ax2.set_title(f"Truck {selected_truck_id} - Speed & Temp")
fig2.autofmt_xdate()
st.pyplot(fig2)

# --- Export CSV ---
st.markdown("### 📤 Export")
if st.button("📁 Export This Truck's Anomaly Data to CSV"):
    st.download_button(
        label="📥 Download CSV",
        data=truck_df.reset_index().to_csv(index=False).encode(),
        file_name=f"anomaly_truck_{selected_truck_id}.csv",
        mime='text/csv'
    )

st.toast("Anomaly analysis complete.")
