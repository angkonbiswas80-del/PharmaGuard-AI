import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://pharmaguard-iot-default-rtdb.firebaseio.com/'
        })
        print("✅ Firebase Connection Successful!")
    except Exception as e:
        print(f"❌ Firebase Error: {e}")

def send_medicine_data(temp, humidity):
    try:
        ref = db.reference('medicine_logs')
        ref.push({
            'temperature': temp,
            'humidity': humidity,
            'status': 'Safe' if 2 <= temp <= 8 else 'Alert',
            'timestamp': {'.sv': 'timestamp'}
        })
        print(f"✅ Data Sent to Cloud: {temp}°C")
    except Exception as e:
        print(f"❌ Cloud Error: {e}")