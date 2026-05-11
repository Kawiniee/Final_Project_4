import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

def init_firebase():
    if not firebase_admin._apps:
        try:
            key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase_key.json')
            db_url = os.getenv('FIREBASE_DB_URL')
            if db_url:
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': db_url
                })
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            return False
    return True

def log_to_firebase(path: str, data: dict):
    try:
        init_firebase()
        ref = db.reference(path)
        ref.push(data)
    except Exception as e:
        print(f"Firebase log error: {e}")