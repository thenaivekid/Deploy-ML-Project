from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load("xgboost_california_housing_model.pkl")

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Define the request body
class CaliforniaHouseRequest(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


@app.post("/predict")
def predict(request: CaliforniaHouseRequest):
    data = [
            [
                request.MedInc,
                request.HouseAge,
                request.AveRooms,
                request.AveBedrms,
                request.Population,
                request.AveOccup,
                request.Latitude,
                request.Longitude,
            ]
        ]
    print(data)
    print()
    prediction = model.predict(
        pd.DataFrame(
            data,
            columns=[
                "MedInc",
                "HouseAge",
                "AveRooms",
                "AveBedrms",
                "Population",
                "AveOccup",
                "Latitude",
                "Longitude",
            ],
        )
    )
    
    return {"prediction": prediction.tolist()[0]*100000}
