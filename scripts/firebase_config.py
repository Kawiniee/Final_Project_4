import os
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

try:
    import firebase_admin
    from firebase_admin import credentials, db
except Exception:
    firebase_admin = None
    credentials = None
    db = None


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _firebase_ready():
    if firebase_admin is None or credentials is None or db is None:
        return False

    key_path = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")
    db_url = os.getenv("FIREBASE_DB_URL")
    if not db_url or not key_path:
        return False
    if not os.path.exists(key_path):
        return False
    return True


def init_firebase():
    if firebase_admin is None:
        return False

    if firebase_admin._apps:
        return True

    try:
        if not _firebase_ready():
            return False

        key_path = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")
        db_url = os.getenv("FIREBASE_DB_URL")
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {"databaseURL": db_url})
        return True
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        return False

def log_to_firebase(path: str, data: dict):
    try:
        if not init_firebase():
            return False
        ref = db.reference(path)
        ref.push(data)
        return True
    except Exception as e:
        print(f"Firebase log error: {e}")
        return False


def build_event_payload(mode: str, input_data: dict, prediction_data: dict, source: dict | None = None):
    payload = {
        "mode": mode,
        "timestamp_utc": _utc_now(),
        "input": input_data,
        "prediction": prediction_data,
    }
    if source:
        payload["source"] = source
    return payload
