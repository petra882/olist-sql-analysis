from fastapi import FastAPI
from pydantic import BaseModel
import joblib


review_model = joblib.load("fast_api/review_model.pkl")

class PredictValue(BaseModel):
    price: float
    freight_value: float
    payment_value: float

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello world"}
@app.post("/predict")
async def predict(request: PredictValue):
    features = [[request.price, request.freight_value, request.payment_value]]
    predict = review_model.predict(features)
    return{"predicted_score": int(predict[0])}