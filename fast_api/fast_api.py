import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

encoder = joblib.load("fast_api/encoder.pkl")
review_model = joblib.load("fast_api/review_model_v2.pkl")

class PredictValue(BaseModel):
    price: float
    freight_value: float
    payment_value: float
    delivery_time: float
    product_category_name: str
    seller_state: str

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello world"}
@app.post("/predict")
async def predict(request: PredictValue):
    numeric_features = [[request.price, request.freight_value, request.payment_value,
                 request.delivery_time]]
    str_features = [[request.product_category_name, request.seller_state]]
    str_features_encoded = encoder.transform(str_features)
    features = np.hstack([numeric_features, str_features_encoded])
    predict = review_model.predict(features)
    return{"predicted_score": int(predict[0])}