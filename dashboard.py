import streamlit as st
import pandas as pd
from firebase_admin import db, credentials, initialize_app
import firebase_admin
import time

# 1. Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {'databaseURL': 'https://pharmaguard-iot-default-rtdb.firebaseio.com/'})

st.set_page_config(page_title="PharmaGuard AI Monitor", layout="wide")
st.title("🛡️ PharmaGuard: Live Real-Time Dashboard")

# 2. Fetch Data
data = db.reference('medicine_logs').order_by_key().limit_to_last(20).get()

if data:
    df = pd.DataFrame(list(data.values()))
    
    # 3. Handle Missing Columns (Error Prevention)
    # Ensure all keys exist to avoid KeyError
    required_cols = ['temp', 'hum', 'lid', 'shock', 'prediction', 'traffic', 'time']
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0 if col in ['temp', 'hum', 'shock'] else "N/A"

    latest = df.iloc[-1]

    # 4. Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🌡️ Temperature", f"{latest['temp']}°C")
    col2.metric("💧 Humidity", f"{latest['hum']}%")
    col3.metric("📦 Lid Status", latest['lid'])
    col4.metric("🫨 Shock Force", f"{latest['shock']}G")
    col5.metric("🚦 Traffic", latest['traffic'])

    st.markdown("---")

    # 5. Charts Row
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("Temperature Trend")
        st.line_chart(df.set_index('time')['temp'], color="#FF4B4B")
    with chart_col2:
        st.subheader("Humidity Trend")
        st.line_chart(df.set_index('time')['hum'], color="#0072B2")

    # 6. Table Row
    st.subheader("📋 Recent Activity Logs")
    display_cols = ['time', 'temp', 'hum', 'lid', 'shock', 'prediction', 'traffic']
    st.table(df[display_cols].tail(10))

    # AI Advice
    st.info(f"🤖 **AI Logistic Advice:** {latest.get('advice', 'Gathering advice...')}")

else:
    st.warning("🔄 Waiting for Live Data... Please run main.py")

# 7. Auto-refresh
time.sleep(5)
st.rerun()