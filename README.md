# 💊 PharmaGuard AI: IoT-Powered Cold Chain & Security Tracker

## 🚀 [Live Dashboard Demo](https://pharmaguard-ai-njdn.onrender.com)
*(Note: The live link might take 30-40 seconds to load if it's been inactive.)*

**PharmaGuard AI** is a real-time IoT solution designed for monitoring the pharmaceutical cold chain.

---

## 📸 Project Showcase

### 1. Real-time Metrics & Temperature Trend
![PharmaGuard Dashboard Preview 1](dashboard_view1.png)  
*(Current Temperature, Humidity, and Trend Line Chart)*

### 2. Full Dashboard View
![PharmaGuard Dashboard Preview 2](dashboard_view2.png)  

### 3. ML Prediction — Live Terminal Output
![ML Terminal Output](pharmaguard_ml_terminal.png)

### 📊 Dashboard Visuals
|Dashbord Overview|| Live Trends | Data Log History |
|---|---|
| ![Dashboard](dashboard_Newview1.png)(dashboard_Newview2.png) | ![Logs](Datalogs_view.png) |

---

## 🌟 Key Features
* **Live Dashboard:** Interactive visualization of temperature, humidity, and physical security.
* **Tamper Detection:** Real-time monitoring of "Lid Status".
* **Impact Sensing:** Shock force (G-force) monitoring.
* **Intelligent Alerts:** Automated warnings when conditions breach safety limits (2°C - 8°C).

## ⚙️ Technical Setup
1. **Installation:**
   ```bash
   python -m pip install -r requirements.txt
2.   ​Execution: - Start monitor: python main.py
​Launch dashboard: python -m streamlit run dashboard.py