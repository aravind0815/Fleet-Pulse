# 🚛 FleetPulse: AI-Powered Truck Breakdown Prediction Dashboard

> Built for the future of fleet management. 
> Powered by real-time data, machine learning, and intelligent design.

---

## 📌 About the Project

FleetPulse is a full-stack, AI-driven diagnostics and visualization system for truck fleets. Designed to simulate and track sensor data in real-time, it predicts breakdown risks using ML models and presents interactive analytics through a professional-grade Streamlit dashboard.

🔍 **Key Features:**
- Real-time data ingestion via Kafka
- Predictive ML model using rolling sensor window
- Interactive dashboards with Streamlit
- PostgreSQL backend for stateful analytics
- Live geolocation map, anomaly detection, truck profiling
- Modern design, animations, and chatbot assistant

---

## 🚨 Problem Statement
Fleet operators today face critical challenges with unplanned truck breakdowns, which cause:
- Unexpected delays in logistics and delivery timelines
- Costly emergency repairs
- Safety risks for drivers and cargo
- A lack of real-time diagnostic intelligence to prevent failures before they occur
- Despite advancements in GPS and vehicle telemetry, most fleet monitoring systems are reactive—they only report problems after they happen. There’s no predictive intelligence that enables preemptive maintenance decisions.

---

🧠 Our Solution: FleetPulse – AI-Powered Truck Breakdown Intelligence
FleetPulse is a real-time predictive maintenance platform built with Kafka, PySpark, PostgreSQL, and Streamlit, offering:

📡 Live Telemetry Ingestion
Simulated sensor data from 10+ trucks streamed via Kafka and processed in Spark.

⚙️ Real-Time ML Predictions
AI model (Logistic Regression/XGBoost) predicts breakdown risk using a rolling window of speed & temperature data.

🖥️ Interactive Dashboard
Built in Streamlit with:

- 📊 Overview KPIs & trend charts
- 🛰️ Live GPS map of risky trucks
- 📈 Anomaly plots (spikes in speed/temp)
- 📘 Truck diagnostic timelines
- 🤖 ML Inference tool for simulations
- 📝 Downloadable fleet reports
- ☁️ Cloud-Ready & Auto-Updating

Deployed on Streamlit Cloud with Render PostgreSQL backend.

---

## 📂 Project Structure

```bash
FleetPulse/
├── spark_streaming_consumer.py     # Kafka + Spark ML pipeline
├── truck_data_simulator.py         # Truck sensor data simulator
├── dashboard/
│   ├── app.py                      # Streamlit dashboard entry point
│   └── pages/
│       ├── overview.py             # KPI summary + risk distribution
│       ├── anomalies.py            # Anomaly detection graphs
│       ├── live_map.py             # Real-time geolocation map
│       ├── truck_profile.py        # Per-truck diagnostics
│       ├── ml_interface.py         # Manual risk prediction using sliders
│       └── report.py               # High-risk incidents report
├── utils/
│   ├── db.py                       # PostgreSQL connection logic
│   ├── ml.py                       # ML model loader/inference logic
│   └── styles.py                   # Custom CSS & theming
├── requirements.txt
└── README.md
```

---

## 🤖 AI-Powered Breakdown Prediction

FleetPulse uses a **Random Forest Classifier** trained on rolling 5-sample averages and standard deviations of truck sensor readings (temperature & speed). 

ML Pipeline:
- Feature engineering on sensor time windows
- Real-time inference in Spark using `joblib`
- Risk score computed and visualized live

---

## ⚙️ Technologies Used

| Layer              | Tools                                   |
|-------------------|------------------------------------------|
| Data Simulation    | Python, Kafka Producer                   |
| Stream Processing  | PySpark Structured Streaming             |
| ML Model           | Scikit-learn, pandas, joblib             |
| Data Storage       | PostgreSQL                               |
| Dashboard          | Streamlit, PyDeck, Matplotlib            |
| UI Enhancements    | `streamlit-extras`, CSS, animations      |

---

## 🛠️ Setup Instructions

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run Kafka & Zookeeper locally** (or use Docker):
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

3. **Start simulator:**
```bash
python truck_data_simulator.py
```

4. **Start Spark ML consumer:**
```bash
python spark_streaming_consumer.py
```

5. **Launch Dashboard:**
```bash
cd dashboard
streamlit run app.py
```

---

## 📸 Screenshots

# Dashboard Overview
<img width="1510" alt="Screenshot 2025-05-08 at 7 43 28 PM" src="https://github.com/user-attachments/assets/58fed4ab-ad27-49b7-b0ae-678da980d299" />

# Live Map 
<img width="1512" alt="Screenshot 2025-05-08 at 7 44 26 PM" src="https://github.com/user-attachments/assets/9ff4751b-f7bc-49ce-8fcf-f9be3d55ca74" />

# ML Panel
<img width="1512" alt="Screenshot 2025-05-08 at 7 45 00 PM" src="https://github.com/user-attachments/assets/6ec46dca-2579-41b9-9b61-69926c766ec5" />

# Truck Profile
<img width="1512" alt="Screenshot 2025-05-08 at 7 45 40 PM" src="https://github.com/user-attachments/assets/1f118fa0-462c-4d7c-874b-efe238120eb0" />

---

## 🌟 Highlights

✅ AI-assisted diagnostics panel with predictive sliders  
✅ Real-time GPS mapping with interactive tooltips  
✅ Dark-themed animations and styling for modern UX  
✅ Chatbot and feedback module integration  
✅ Sensible, modular code structure for extensibility

---

👨‍💻 Maintainer
Aravind Kalyan Sivakumar
NJIT | Data Scientist | AI/ML Enthusiast
🌐 [LinkedIn](https://www.linkedin.com/in/aravindkalyan007/) • [GitHub](https://github.com/aravind0815)

## 🧠 Future Scope

- Real-time vehicle health via CAN Bus integration
- Predictive alerting to drivers via SMS/email
- Integration with cloud-native Kafka (MSK / Confluent)
- Deployment-ready Docker/CI pipeline

---

## 📄 License

This project is licensed under the MIT License.
