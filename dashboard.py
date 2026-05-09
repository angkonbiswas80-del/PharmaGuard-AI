import os
import json
import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import db, credentials, initialize_app
import time

# 1. Page Configuration (Keep only one instance of st.set_page_config)
st.set_page_config(
    page_title="PharmaGuard AI - Cold Chain Monitor",
    page_icon="🛡️",
    layout="wide"
)

# 2. Firebase Initialization with Environment Variable
if not firebase_admin._apps:
    # Get the JSON string from Render Environment Variable
    if "FIREBASE_SERVICE_ACCOUNT" in os.environ:
        # Load the JSON data from the variable
        service_info = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT"))
        cred = credentials.Certificate(service_info)
    else:
        # Fallback for local testing if the file exists
        cred = credentials.Certificate("serviceAccountKey.json")
    
    initialize_app(cred, {
        'databaseURL': 'https://pharmaguard-iot-default-rtdb.firebaseio.com/'
    })

# 3. Header Section
st.title("🛡️ PharmaGuard: Smart Asset Tracker (Saga Replica)")
st.markdown("### Real-time Medicine Cold-Chain & Security Monitoring")

# 4. Data Fetching Function
def fetch_logs():
    try:
        # Fetch last 20 entries from Firebase
        data = db.reference('medicine_logs').order_by_key().limit_to_last(20).get()
        if data:
            # Convert dictionary to DataFrame
            df_data = pd.DataFrame(list(data.values()))
            # Sort by timestamp if available to ensure correct chart plotting
            if 'timestamp' in df_data.columns:
                df_data = df_data.sort_values('timestamp')
            return df_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return pd.DataFrame()

# 5. UI Logic
df = fetch_logs()

if not df.empty:
    latest = df.iloc[-1]
    
    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ Temperature", f"{latest['temperature']}°C")
    
    with col2:
        st.metric("💧 Humidity", f"{latest['humidity']}%")
        
    with col3:
        # Tamper Alert Logic
        is_open = str(latest['lid_status']).upper() == "OPEN"
        st.metric("📦 Lid Status", f"{'🔴' if is_open else '🟢'} {latest['lid_status']}")

    with col4:
        # Impact Alert Logic
        is_shock = float(latest['shock_force']) > 2.0
        st.metric("🫨 Shock Force", f"{'⚠️' if is_shock else '✅'} {latest['shock_force']}G")

    # Visualizations
    st.divider()
    st.subheader("Live Tracking Trends")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("**Temperature Stability**")
        st.line_chart(df.set_index('timestamp')['temperature'])
    
    with chart_col2:
        st.write("**Impact/Shock Force Log**")
        st.area_chart(df.set_index('timestamp')['shock_force'])

    # Data Table
    st.divider()
    st.subheader("Recent Data Logs")
    st.dataframe(df.tail(10), use_container_width=True)

else:
    st.info("🔄 Waiting for incoming data from Firebase... Please ensure your IoT simulator (main.py) is running.")

# 6. Auto-Refresh logic (Every 5 seconds is safer for Render's free tier)
time.sleep(5)
st.rerun()