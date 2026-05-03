import joblib
import pandas as pd
from typing import Dict


# =========================
# LOAD MODEL
# =========================
customer_model = joblib.load("app/customer_model.pkl")
platform_model = joblib.load("app/platform_model.pkl")
time_model = joblib.load("app/time_model.pkl")

feature_cols = joblib.load("app/feature_cols.pkl")


# =========================
# HELPER: NORMALIZE INPUT
# =========================
def normalize_input(data: Dict) -> Dict:
    """
    ทำให้ input ตรง format ตอน train
    """
    return {
        "Age": int(data.get("age", 0)),
        "Sex": str(data.get("sex", "")).strip().title(),
        "Profession": str(data.get("profession", "")).strip().title(),
        "Province": str(data.get("province", "")).strip().title(),
    }


# =========================
# PREPROCESS (FIX ตัวจริง)
# =========================
def preprocess(input_data: Dict) -> pd.DataFrame:

    data = normalize_input(input_data)

    df = pd.DataFrame([data])

    # ---------- ONE HOT ----------
    df = pd.get_dummies(df)

    # ---------- ALIGN COLUMN ----------
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_cols]

    # ---------- DEBUG ----------
    # เช็คว่ามี feature ที่เป็น 1 จริงไหม
    active_features = df.loc[0][df.loc[0] == 1].index.tolist()
    print("ACTIVE FEATURES:", active_features[:10])

    if len(active_features) == 0:
        print("⚠️ WARNING: All features are 0 → input ไม่ match training")

    return df


# =========================
# CLEAN LABEL
# =========================
def clean_label(label: str) -> str:
    if "Cluster_ID_" in label:
        return label.replace("Cluster_ID_", "")
    elif "S_Occasion_" in label:
        return label.replace("S_Occasion_", "")
    elif "S_Time(weekday)_" in label:
        return label.replace("S_Time(weekday)_", "")
    return label


# =========================
# PIPELINE
# =========================
def predict_pipeline(input_data: Dict) -> Dict:

    X = preprocess(input_data)

    # -------- CUSTOMER --------
    customer_raw = customer_model.predict(X)[0]
    customer = clean_label(customer_raw)

    # -------- PLATFORM --------
    platform_raw = platform_model.predict(X)[0]
    platform = clean_label(platform_raw)

    # -------- TIME --------
    time_raw = time_model.predict(X)[0]
    time = clean_label(time_raw)

    print("PREDICT RESULT:", customer, platform, time)

    return {
        "customer_segment": customer,
        "recommended_platform": platform,
        "best_ad_time": time
    }