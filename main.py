import os
import random
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import numpy as np
from sklearn.linear_model import LinearRegression
from groq import Groq
from dotenv import load_dotenv

# --- 1. SETUP ---
load_dotenv() 
api_key = os.getenv("GROQ_API_KEY") 

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pharmaguard-iot-default-rtdb.firebaseio.com/'
    })

client = Groq(api_key=api_key)
ref = db.reference('medicine_logs')
temp_history = []

# --- 2. LOGIC FUNCTIONS ---
def predict_next_temp():
    if len(temp_history) < 3: 
        return "Analyzing..."
    X = np.array(range(len(temp_history))).reshape(-1, 1)
    y = np.array(temp_history)
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[len(temp_history)]])[0]
    return round(float(prediction), 2)

def get_ai_advice(temp, hum, lid):
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Temp: {temp}C, Humidity: {hum}%, Lid: {lid}. Give 1-sentence advice."}],
            model="llama-3.3-70b-versatile",
            max_tokens=40
        )
        return completion.choices[0].message.content.strip()
    except:
        return "AI Agent: Status unavailable"

# --- 3. MONITORING LOOP ---
print("🚀 PharmaGuard AI: Monitoring Online (Humidity & ML Included)...")

try:
    while True:
        # Generating Data
        temp = round(random.uniform(2.0, 8.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)
        lid = "OPEN" if random.random() < 0.05 else "CLOSED"
        shock = round(random.uniform(0.1, 0.9), 2)
        traffic = random.choice(["Smooth", "Moderate Jam", "Heavy Traffic"])
        
        temp_history.append(temp)
        if len(temp_history) > 10: temp_history.pop(0)
        
        # Calculations
        prediction = predict_next_temp()
        advice = get_ai_advice(temp, humidity, lid)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Push to Firebase (Formatted for Dashboard)
        ref.push({
            "temp": temp,
            "hum": humidity,
            "lid": lid,
            "shock": shock,
            "prediction": prediction,
            "advice": advice,
            "time": timestamp,
            "traffic": traffic
        })

        # --- EXACT TERMINAL VIEW AS PER IMAGE ---
        print("-" * 60)
        print(f"✅ [{timestamp}] Temp: {temp}C | Hum: {humidity}% | Lid: {lid} | Shock: {shock}G")
        print(f"   ML Prediction: {prediction}C | Traffic: {traffic}")
        print(f"   AI Agent: {advice}")
        
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 PharmaGuard System Shutting Down...")