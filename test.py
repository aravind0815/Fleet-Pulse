import joblib
import pandas as pd

# 🔁 Load the saved model
model = joblib.load("rolling_breakdown_predictor.pkl")

# 🧪 Create synthetic risky and non-risky feature sets
test_data = pd.DataFrame([
    {
        "temp_avg_5": 105,   # high average temperature
        "speed_avg_5": 65,
        "temp_std_5": 6.5,   # high variation
        "speed_std_5": 6.2
    },
    {
        "temp_avg_5": 85,    # normal temperature
        "speed_avg_5": 60,
        "temp_std_5": 1.5,
        "speed_std_5": 2.2
    }
])

# 🔮 Run predictions
proba = model.predict_proba(test_data)
predictions = model.predict(test_data)

# 📊 Display output
for i, (p, prob) in enumerate(zip(predictions, proba)):
    print(f"Test Case {i+1}:")
    print(f"  ➤ Features: {test_data.iloc[i].to_dict()}")
    print(f"  ➤ Predicted Breakdown: {p}")
    print(f"  ➤ Breakdown Risk Score: {prob[1]:.4f}")
    print()
