import joblib
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

# --- Load Model ---
_model = None

def load_model():
    global _model
    if _model is None:
        model_path = os.path.join("models", "rolling_breakdown_predictor.pkl")
        _model = joblib.load(model_path)
    return _model

# --- AI-Enhanced Predictor ---
def predict_breakdown_risk(temp_list, speed_list):
    try:
        if len(temp_list) != 5 or len(speed_list) != 5:
            return None, "❌ Please provide exactly 5 readings each for temperature and speed."

        features = pd.DataFrame([{
            "temp_avg_5": np.mean(temp_list),
            "speed_avg_5": np.mean(speed_list),
            "temp_std_5": np.std(temp_list),
            "speed_std_5": np.std(speed_list)
        }])

        model = load_model()
        risk_score = model.predict_proba(features)[0][1]

        # Generate AI-based feedback
        feedback = ""
        if risk_score > 0.9:
            feedback = "🚨 Critical pattern detected: historical data suggests high failure correlation."
        elif risk_score > 0.7:
            feedback = "⚠️ Warning: Conditions similar to previous breakdown events."
        elif risk_score > 0.4:
            feedback = "🟡 Moderate risk: monitor conditions regularly."
        else:
            feedback = "✅ Normal operating range."

        return float(risk_score), feedback

    except Exception as e:
        return None, f"Error: {str(e)}"

# --- Advanced Feedback Utility for Other Pages ---
def get_advanced_risk_commentary(risk):
    if risk > 0.9:
        return "🔴 System Alert: Imminent breakdown likelihood. Prioritize urgent inspection."
    elif risk > 0.7:
        return "🟠 Elevated risk trend observed. Operational caution recommended."
    elif risk > 0.5:
        return "🟡 Mild warning zone. Parameters nearing risk thresholds."
    elif risk > 0.3:
        return "🟢 Within tolerance, but risk trajectory is increasing."
    else:
        return "✅ Optimal performance. No immediate actions needed."

# --- For Report or Truck Profile Integration ---
def generate_diagnostic_summary(df):
    try:
        if df.empty:
            return "No data to summarize."

        recent = df.tail(1).iloc[0]
        comment = get_advanced_risk_commentary(recent['breakdown_risk'])

        summary = f"""
        **Latest Snapshot**:
        - 🕒 Timestamp: `{recent['timestamp']}`
        - 🚚 Speed: `{recent['speed']} km/h`
        - 🌡️ Temperature: `{recent['temperature']} °C`
        - 📍 Location: ({recent['latitude']}, {recent['longitude']})
        - 💥 Risk Score: `{recent['breakdown_risk']:.2f}`

        **System Intelligence:**
        {comment}
        """
        return summary

    except Exception as e:
        return f"Could not generate diagnostics: {str(e)}"
