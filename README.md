# 💊 PharmaGuard AI: IoT-Powered Cold Chain Monitor

**Real-time Pharmaceutical Cold Chain Monitoring with AI-Powered Insights**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20Dashboard-brightgreen)](https://pharmaguard-ai-njdn.onrender.com)

---

## 🚀 Overview

**PharmaGuard AI** is an intelligent IoT-based solution designed for real-time monitoring of pharmaceutical cold chain shipments and storage. It tracks critical environmental parameters and provides actionable AI-driven insights to ensure medicine quality and regulatory compliance.

---

## ✨ Key Features

- **Real-time Monitoring**: Temperature, Humidity, Lid Status & Shock/G-force
- **AI-Powered Predictions**: Machine Learning model predicts traffic conditions and potential risks
- **Intelligent AI Agent**: Provides contextual advice based on current conditions
- **Live Dashboard**: Beautiful, responsive Streamlit dashboard with trend visualization
- **Tamper Detection**: Real-time lid open/close monitoring
- **Data Logging**: Complete activity history with Firebase integration
- **Alert System**: Automatic warnings when parameters go beyond safe thresholds (2°C - 8°C)

---

## 📸 Project Showcase

### Live Dashboard
![PharmaGuard Live Dashboard](dashboard_view1.png)

### Trends & Analytics
![Temperature & Humidity Trends](dashboard_Newview2.png)

### Activity Logs
![Recent Activity Logs](Datalogs_view.png)

### Terminal Output with AI Insights
![ML Terminal with AI Agent](pharmaguard_ml_terminal.png)

### 📊 Dashboard Visuals
|Dashboard Overview|| Live Trends | Data Log History |
|---|---|---|
![Dashboard](dashboard_Newview1.png) ![Tends](dashboard_Newview2.png) | ![Logs](Datalogs_view.png) |

### 🚦 Real-Time Traffic & Smart Alert Optimization
PharmaGuard uses the TomTom Traffic API to adaptively optimize transit safety based on live Dhaka traffic conditions.

| Traffic State | System Logs & AI Agent Recommendations |
|---|---|
| **Smooth** | <img src="traffic_smooth_log.png"> |
| **Moderate Jam** | <img src="traffic_moderate_log.png"> |
| **Heavy Traffic** | <img src="traffic_heavy_log.png"> |

### 📧 Automated Notification System
When the system encounters critical routing gridlocks (`Heavy Traffic`) or unauthorized access (`Lid: OPEN`), it immediately dispatches dynamic HTML alerts to stakeholders.

<p align="center">
  <img src="mobile_notification_alert.png" alt="Mobile Notification Alert"/>
</p>

### 📧 Automated Notification System
PharmaGuard instantly dispatches professional HTML alerts when critical operational exceptions occur (e.g., severe gridlocks or unauthorized container access).

| Alert Type | Mobile Push Notification (Gmail) | System Telemetry Logs |
|---|---|---|
| **Security Breach (`Lid: OPEN`)** | <img src="lid_open_mobile_alert.jpg"> | <img src="lid_open_terminal_log.png"> |


## 🛠️ Tech Stack

- **Backend**: Python
- **IoT Simulation**: Custom sensor data simulation
- **Machine Learning**: Scikit-learn (Linear Regression + Classification)
- **Dashboard**: Streamlit
- **Database**: Firebase (Firestore)
- **Visualization**: Plotly
- **Deployment**: Render

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/angkonbiswas80-del/PharmaGuard-AI.git
cd PharmaGuard-AI

# 2. Create virtual environment (Recommended)
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the monitor
python main.py

# 5. Run the dashboard (in new terminal)
streamlit run dashboard.py
