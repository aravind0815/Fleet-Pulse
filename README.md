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

## 🚀 Live Demo Preview

![FleetPulse Dashboard Demo](https://your-demo-preview-link.com)

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

| Dashboard Overview | Live Map |
|--------------------|----------|
| ![Overview](assets/overview.png) | ![Live Map](assets/livemap.png) |

| ML Panel | Truck Profile |
|----------|---------------|
| ![ML](assets/mlpanel.png) | ![Profile](assets/truckprofile.png) |

---

## 🌟 Highlights

✅ AI-assisted diagnostics panel with predictive sliders  
✅ Real-time GPS mapping with interactive tooltips  
✅ Dark-themed animations and styling for modern UX  
✅ Chatbot and feedback module integration  
✅ Sensible, modular code structure for extensibility

---

## 📫 Contact / Connect

Made with 💙 by [Aravind Kalyan Sivakumar](https://github.com/aravind0815)

> For collaboration, feedback or hiring inquiries, feel free to reach out on [LinkedIn](https://www.linkedin.com/in/aravindkalyan007/)

---

## 🧠 Future Scope

- Real-time vehicle health via CAN Bus integration
- Predictive alerting to drivers via SMS/email
- Integration with cloud-native Kafka (MSK / Confluent)
- Deployment-ready Docker/CI pipeline

---

## 📄 License

This project is licensed under the MIT License.
