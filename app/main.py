from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schema import InputData, FeedbackData
from app.model_utils import predict_pipeline
import pandas as pd
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict/all")
def predict(data: InputData):
    return predict_pipeline(data.dict())


# ⭐ เพิ่มตรงนี้ (เก็บ feedback)
@app.post("/feedback")
def save_feedback(data: FeedbackData):

    df = pd.DataFrame([data.dict()])

    file_path = "feedback_data.csv"

    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

    return {"message": "feedback saved"}