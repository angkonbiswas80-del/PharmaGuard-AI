import streamlit as st
import pandas as pd
from firebase_admin import db, credentials, initialize_app
import firebase_admin
import time

# 1. Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {
        'databaseURL': 'https://pharmaguard-iot-default-rtdb.firebaseio.com/'
    })

# Page Configuration
st.set_page_config(page_title="PharmaGuard: Saga Replica", layout="wide")

st.title("🛡️ PharmaGuard: Smart Asset Tracker (Saga Replica)")
st.markdown("Real-time Medicine Cold-Chain & Security Monitoring")

# 2. Data Fetching Function
def fetch_logs():
    try:
        # Fetch last 20 entries
        data = db.reference('medicine_logs').order_by_key().limit_to_last(20).get()
        if data:
            return pd.DataFrame(list(data.values()))
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return pd.DataFrame()

# Get data
df = fetch_logs()

if not df.empty:
    latest = df.iloc[-1]
    
    # --- Live Status Indicators ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ Temperature", f"{latest['temperature']}°C")
    
    with col2:
        st.metric("💧 Humidity", f"{latest['humidity']}%")
        
    with col3:
        # Tamper Alert Logic
        is_open = latest['lid_status'] == "OPEN"
        st.metric("📦 Lid Status", f"{'🔴' if is_open else '🟢'} {latest['lid_status']}")

    with col4:
        # Impact Alert Logic
        is_shock = float(latest['shock_force']) > 2.0
        st.metric("🫨 Shock Force", f"{'⚠️' if is_shock else '✅'} {latest['shock_force']}G")

    # --- Trend Visualization ---
    st.subheader("Live Tracking Trends")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("Temperature Stability")
        st.line_chart(df.set_index('timestamp')['temperature'])
    
    with chart_col2:
        st.write("Impact/Shock Force Log")
        st.area_chart(df.set_index('timestamp')['shock_force'])

    # --- Recent Logs Table ---
    st.subheader("Data Log History")
    st.dataframe(df.tail(10), use_container_width='stretch')

else:
    st.info("Waiting for incoming data from Firebase... Start main.py first.")

# 3. Auto-Refresh every 2 seconds
time.sleep(2)
st.rerun()