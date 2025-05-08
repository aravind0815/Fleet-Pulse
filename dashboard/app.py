# import streamlit as st
# from utils.styles import set_custom_theme
# from datetime import datetime

# # --- Page Config ---
# st.set_page_config(
#     page_title="FleetPulse - Truck Breakdown Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Apply Theme ---
# set_custom_theme()

# # --- Custom CSS for sleek design ---
# st.markdown("""
# <style>
# .big-title {
#     font-size: 42px;
#     font-weight: bold;
#     color: #1abc9c;
# }
# .subtitle {
#     font-size: 20px;
#     color: #7f8c8d;
# }
# .feature-box {
#     background-color: #f9f9f9;
#     padding: 1.2rem;
#     border-radius: 12px;
#     box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     margin-bottom: 1.5rem;
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Header ---
# st.markdown('<p class="big-title">🧠 FleetPulse AI-Powered Breakdown Intelligence</p>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Welcome to your advanced diagnostics and decision support dashboard.</p>', unsafe_allow_html=True)

# # --- Summary KPIs ---
# col1, col2, col3 = st.columns(3)
# col1.metric("🚛 Total Trucks Tracked", "10")
# col2.metric("⚠️ High Risk Alerts (24h)", "3")
# col3.metric("📡 Data Stream Status", "✅ Live")

# st.markdown("---")

# # --- Guided Module Selection ---
# st.subheader("📍 What would you like to explore today?")
# colA, colB, colC = st.columns(3)

# with colA:
#     st.markdown('<div class="feature-box">', unsafe_allow_html=True)
#     st.markdown("### 📊 **Overview**")
#     st.markdown("Visualize active trucks, risk distributions, and recent breakdowns. Ideal for a quick glance at fleet health.")
#     if st.button("Go to Overview"):
#         st.switch_page("pages/overview.py")
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('<div class="feature-box">', unsafe_allow_html=True)
#     st.markdown("### 🛰️ **Live Map**")
#     st.markdown("View current truck positions and breakdown risk geospatially in real time.")
#     if st.button("Launch Live Map"):
#         st.switch_page("pages/live_map.py")
#     st.markdown('</div>', unsafe_allow_html=True)

# with colB:
#     st.markdown('<div class="feature-box">', unsafe_allow_html=True)
#     st.markdown("### 📈 **Anomaly Detector**")
#     st.markdown("Analyze abnormal spikes in temperature or speed. Great for spotting risky patterns.")
#     if st.button("Analyze Anomalies"):
#         st.switch_page("pages/anomalies.py")
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('<div class="feature-box">', unsafe_allow_html=True)
#     st.markdown("### 🧠 **ML Inference Panel**")
#     st.markdown("Use AI to predict truck failure risk based on live or simulated sensor data.")
#     if st.button("Try AI Prediction"):
#         st.switch_page("pages/ml_interface.py")
#     st.markdown('</div>', unsafe_allow_html=True)

# # --- Footer ---
# st.markdown("---")
# st.markdown("💡 *Powered by real-time sensor data and machine learning for proactive fleet maintenance.*")

# st.toast("FleetPulse is standing by with real-time intelligence.")


import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header
from streamlit_extras.buy_me_a_coffee import button as coffee_button

# Set page config
st.set_page_config(
    page_title="FleetPulse - Truck Breakdown Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS to improve sidebar aesthetics
def sidebar_style():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #1f1f2e, #2a2a3d);
            color: white;
        }
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

sidebar_style()

# Load theme
from utils.styles import set_custom_theme
set_custom_theme()

# Hero Title with animation
colored_header("FleetPulse Dashboard", description="Predictive Maintenance Intelligence for Smart Fleets", color_name="violet-70")

st.markdown("""
    <h1 style="
        text-align: center;
        font-size: 2.4em;
        background: -webkit-linear-gradient(45deg, #9B59B6, #2ECC71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s infinite;
    ">
        Your trucks. Our AI. Zero breakdowns.
    </h1>
    <style>
    @keyframes pulse {
      0% { transform: scale(1); opacity: 0.9; }
      50% { transform: scale(1.05); opacity: 1; }
      100% { transform: scale(1); opacity: 0.9; }
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="text-align:center; margin-top:20px; font-size:18px;">
        Welcome to FleetPulse – the smart dashboard for real-time breakdown risk tracking, truck diagnostics, and anomaly detection. <br><br>
        Use the interactive cards below to dive into each module and optimize your fleet's performance.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Navigation Buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/overview.py", label="📊 Fleet Overview", icon="📈")
    st.page_link("pages/anomalies.py", label="🚨 Anomaly Detection", icon="⚠️")

with col2:
    st.page_link("pages/live_map.py", label="🛰️ Live Truck Map", icon="🗺️")
    st.page_link("pages/ml_interface.py", label="🤖 ML Risk Inference", icon="🧠")

with col3:
    st.page_link("pages/truck_profile.py", label="📘 Truck Profile View", icon="🚚")
    st.page_link("pages/report.py", label="📝 Summary Reports", icon="📋")

# Bonus animation (optional)
rain(
    emoji=" ",
    font_size=25,
    falling_speed=5,
    animation_length="infinite"
)

# Sidebar content
st.sidebar.title("📊 Dashboard Sections")
st.sidebar.markdown("""
- **Overview**: Summary stats & recent breakdowns  
- **Live Map**: Real-time truck locations & risk  
- **Anomalies**: Graph spikes in speed/temperature  
- **Truck Profile**: Drill into each truck  
- **ML Inference**: Try the risk prediction model  
- **Reports**: Download diagnostic summaries  
""")

# if show_feedback:
#     st.markdown("""
#         <div style="text-align:center; margin-top: 30px;">
#             <a href="https://forms.gle/YOUR_GOOGLE_FORM_ID" target="_blank" style="
#                 background-color: #6c5ce7;
#                 color: white;
#                 padding: 12px 24px;
#                 border-radius: 30px;
#                 text-decoration: none;
#                 font-weight: bold;
#                 box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
#             ">
#                 💬 Give Feedback & Shape FleetPulse
#             </a>
#         </div>
#     """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; margin-top: 30px;">
        <a href="https://github.com/aravind0815/" target="_blank" style="
            color: #fff;
            background: linear-gradient(45deg, #8e44ad, #2980b9);
            padding: 12px 24px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
        ">
            ✨ GitHub Profile
        </a>
    </div>
""", unsafe_allow_html=True)

