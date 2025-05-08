import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load dataset
df = pd.read_csv("training_rolling_data.csv")

# Features and label
X = df[["temp_avg_5", "speed_avg_5", "temp_std_5", "speed_std_5"]]
y = df["breakdown"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n🔍 Classification Report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "rolling_breakdown_predictor.pkl")
print("✅ Model saved to rolling_breakdown_predictor.pkl")
