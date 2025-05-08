# import streamlit as st
# from utils.ml import predict_breakdown_risk
# from utils.styles import set_custom_theme

# st.set_page_config(page_title="Risk Predictor", layout="centered")
# set_custom_theme()
# st.title("🧠 ML Risk Inference Panel")
# st.markdown("Simulate truck sensor data and get real-time breakdown risk predictions using the trained ML model.")

# # Sliders for user input
# st.subheader("📊 Input 5 Recent Sensor Readings")

# with st.form("risk_form"):
#     col1, col2 = st.columns(2)

#     with col1:
#         temp_list = [st.slider(f"Temperature {i+1} (°C)", 50, 120, 70) for i in range(5)]

#     with col2:
#         speed_list = [st.slider(f"Speed {i+1} (km/h)", 0, 120, 60) for i in range(5)]

#     submitted = st.form_submit_button("🚛 Predict Breakdown Risk")

# if submitted:
#     risk = predict_breakdown_risk(temp_list, speed_list)
#     if risk is not None:
#         st.success(f"🔮 **Predicted Breakdown Risk:** {risk}")
#         if risk > 0.9:
#             st.error("⚠️ High Risk! Immediate Attention Needed")
#         elif risk > 0.7:
#             st.warning("⚠️ Moderate Risk. Monitor Closely.")
#         else:
#             st.info("✅ Low Risk. Truck is healthy.")
#     else:
#         st.warning("Need 5 valid readings to predict.")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.ml import predict_breakdown_risk
from utils.styles import set_custom_theme

# --- Page Setup ---
st.set_page_config(page_title="🧠 AI Breakdown Predictor", layout="centered")
set_custom_theme()

st.title("🚚 Fleet AI Risk Diagnostic Panel")
st.markdown("Enter recent sensor data to simulate truck behavior and get advanced ML-driven risk assessment.")

# --- Input Section ---
st.subheader("📊 Sensor Reading Simulator")
st.markdown("Adjust sliders below to represent recent truck temperature and speed data. The model evaluates risk based on trends and volatility.")

with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        temp_list = [st.slider(f"🌡️ Temperature {i+1} (°C)", 40, 130, 75, key=f"temp_{i}") for i in range(5)]
    with col2:
        speed_list = [st.slider(f"🚀 Speed {i+1} (km/h)", 0, 130, 60, key=f"speed_{i}") for i in range(5)]

    st.markdown("---")
    submitted = st.form_submit_button("🔍 Run AI Risk Prediction")

if submitted:
    with st.spinner("Analyzing sensor trend with AI model..."):
        risk_score = predict_breakdown_risk(temp_list, speed_list)

    if risk_score is not None:
        st.metric(label="🔮 Predicted Breakdown Risk Score", value=f"{risk_score:.2f}")

        # --- Risk Category Indicator ---
        if risk_score > 0.9:
            st.error("⚠️ Critical Risk: Immediate Service Required!")
        elif risk_score > 0.7:
            st.warning("⚠️ Elevated Risk: Monitor Closely.")
        elif risk_score > 0.4:
            st.info("🟡 Mild Risk: Consider Diagnostics.")
        else:
            st.success("✅ Low Risk: Truck is Healthy.")

        # --- Visual Output ---
        st.markdown("### 📈 Sensor Pattern Overview")
        fig, ax1 = plt.subplots()
        ax1.plot(range(1, 6), speed_list, marker='o', label="Speed (km/h)", color="#3498db")
        ax1.set_ylabel("Speed", color="#3498db")

        ax2 = ax1.twinx()
        ax2.plot(range(1, 6), temp_list, marker='s', label="Temperature (°C)", color="#e67e22")
        ax2.set_ylabel("Temperature", color="#e67e22")

        fig.tight_layout()
        st.pyplot(fig)

        # --- Export Option ---
        st.download_button(
            label="⬇️ Export Simulation CSV",
            data=pd.DataFrame({"Speed": speed_list, "Temperature": temp_list}).to_csv(index=False),
            file_name="simulated_readings.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Prediction failed. Please enter valid data.")
