import random
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Setup Firebase Credentials
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pharmaguard-iot-default-rtdb.firebaseio.com/'
})

# Reference to your medicine_logs node
ref = db.reference('medicine_logs')

# ML: Store temperature history
temp_history = []

def predict_next_temperature():
    if len(temp_history) < 3:
        return None
    X = np.array(range(len(temp_history))).reshape(-1, 1)
    y = np.array(temp_history)
    model = LinearRegression()
    model.fit(X, y)
    next_temp = model.predict([[len(temp_history)]])[0]
    return round(next_temp, 2)

def generate_sensor_data():
    global temp_history
    print("🚀 Saga Replica Simulator Started...")
    print("Press Ctrl+C to stop.\n")

    while True:
        # --- Core Temperature Logic ---
        # Simulating standard pharma range 2.0 - 8.0
        temp = round(random.uniform(1.5, 8.5), 2)
        humidity = round(random.uniform(35.0, 50.0), 1)

        # --- Saga Replica: Security Features ---
        # Lid Status: 3% chance it gets opened during transit
        lid_open = random.random() < 0.03

        # Shock Force: Measuring G-force (Standard is low, < 1.0G)
        # 2% chance of a high impact (dropped or hit)
        if random.random() < 0.02:
            shock_g = round(random.uniform(2.5, 5.5), 2)  # High Impact!
        else:
            shock_g = round(random.uniform(0.05, 0.6), 2)  # Normal vibration

        # --- System Logic ---
        status = "Safe"
        # Alert if temperature is out of range OR lid is open OR high shock detected
        if (temp < 2.0 or temp > 8.0) or lid_open or (shock_g > 2.0):
            status = "Alert"

        # --- ML Prediction ---
        temp_history.append(temp)
        predicted_temp = predict_next_temperature()

        ml_warning = False
        if predicted_temp is not None:
            if predicted_temp < 2.0 or predicted_temp > 8.0:
                ml_warning = True
                if status == "Safe":
                    status = "ML-Alert"

        # Create Data Payload
        data = {
            "temperature": temp,
            "humidity": humidity,
            "lid_status": "OPEN" if lid_open else "CLOSED",
            "shock_force": shock_g,
            "status": status,
            "predicted_next_temp": predicted_temp if predicted_temp else "Collecting data...",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

        # Send to Firebase
        try:
            ref.push(data)
            print(f"✅ Temp={temp}°C | Humidity={humidity}% | Lid={data['lid_status']} | Shock={shock_g}G | Status={status}")
            if predicted_temp:
                print(f"   [ML] Predicted next temp: {predicted_temp}°C")
            if ml_warning:
                print(f"   ⚠️  ML WARNING: Next temperature may breach threshold!")
        except Exception as e:
            print(f"❌ Error: {e}")

        # Wait for 2 seconds before next reading
        time.sleep(2)

if __name__ == "__main__":
    generate_sensor_data()