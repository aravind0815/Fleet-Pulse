import streamlit as st

# Title of the dashboard
st.title("🚛 FleetPulse Dashboard")
st.markdown("Select a page from the sidebar to explore truck data insights.")

# Sidebar configuration
st.sidebar.title("📊 Dashboard Sections")
st.sidebar.markdown("""
- **Overview**: Summary stats & recent breakdowns  
- **Live Map**: Real-time truck locations & risk  
- **Anomalies**: Graph spikes in speed/temperature  
- **Truck Profile**: Drill into each truck  
- **ML Inference**: Try the risk prediction model  
""")

# Sidebar navigation
pages = {
    "overview": "overview.py",       # using lowercase for pages
    "live map": "live_map.py",       # using lowercase for pages
    "anomalies": "anomalies.py",     # using lowercase for pages
    "truck profile": "truck_profile.py",  # using lowercase for pages
    "ml inference": "ml_inference.py",    # using lowercase for pages
}

# User selects the page to view (converted to lowercase)
selected_page = st.sidebar.radio("Select a page:", list(pages.keys())).lower()

# Dynamically load the selected page
if selected_page == "overview":
    exec(open("dashboard/pages/overview.py").read())
elif selected_page == "live map":
    exec(open("dashboard/pages/live_map.py").read())
elif selected_page == "anomalies":
    exec(open("dashboard/pages/anomalies.py").read())  # Add logic for anomalies
elif selected_page == "truck profile":
    exec(open("dashboard/pages/truck_profile.py").read())  # Add logic for truck profile
elif selected_page == "ml inference":
    exec(open("dashboard/pages/ml_inference.py").read())  # Add logic for ML Inference






#anomaly
import streamlit as st
import pandas as pd
from utils.db import get_connection

st.set_page_config(page_title="📈 Anomaly Detection", layout="wide")
st.title("📈 Anomaly Detection in Truck Data")
st.markdown("This page highlights unusual patterns in truck temperature and speed data. Spikes and dips could indicate potential issues or risky behavior.")

# Connect and fetch data
conn = get_connection()
query = """
    SELECT truck_id, 
           CAST(timestamp AS timestamp) AS timestamp, 
           speed, temperature, breakdown_risk
    FROM truck_breakdown_logs
    WHERE CAST(timestamp AS timestamp) >= NOW() - INTERVAL '1 day'
    ORDER BY truck_id, CAST(timestamp AS timestamp)
    LIMIT 2000;
"""

df = pd.read_sql(query, conn)

# Show raw sample
st.subheader("Raw Data Sample")
st.dataframe(df.head(20), use_container_width=True)

if df.empty:
    st.warning("No recent truck data found.")
else:
    # Sort for rolling calculations
    df = df.sort_values(by=["truck_id", "timestamp"])

    # Rolling stats (window=5)
    df["temp_avg"] = df.groupby("truck_id")["temperature"].transform(lambda x: x.rolling(window=5).mean())
    df["temp_std"] = df.groupby("truck_id")["temperature"].transform(lambda x: x.rolling(window=5).std())
    df["speed_avg"] = df.groupby("truck_id")["speed"].transform(lambda x: x.rolling(window=5).mean())
    df["speed_std"] = df.groupby("truck_id")["speed"].transform(lambda x: x.rolling(window=5).std())

    # Filter for anomalies (loosened thresholds for testing)
    temp_anomalies = df[df["temp_std"] > 1.0]   # You can adjust back to >5 once working
    speed_anomalies = df[df["speed_std"] > 2.0]

    st.subheader("📊 Anomaly Trends")

    st.line_chart(df.set_index("timestamp")[["speed"]].dropna().sort_index(), height=250)
    st.line_chart(df.set_index("timestamp")[["temperature"]].dropna().sort_index(), height=250)

    with st.expander("🔍 View Anomaly Data"):
        st.markdown("### Temperature Anomalies")
        st.dataframe(temp_anomalies[["truck_id", "timestamp", "speed", "temperature", "breakdown_risk", "temp_avg", "temp_std"]], use_container_width=True)

        st.markdown("### Speed Anomalies")
        st.dataframe(speed_anomalies[["truck_id", "timestamp", "speed", "temperature", "breakdown_risk", "speed_avg", "speed_std"]], use_container_width=True)

    st.success(f"✅ {len(temp_anomalies)} temperature anomalies and {len(speed_anomalies)} speed anomalies detected.")
