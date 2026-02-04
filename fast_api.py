import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# Setup initial
app = FastAPI()
model: mlflow.pyfunc.PyFuncModel = None

# Define the tracking URI for MLflow
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_URI)

# Pydantic models for strict typing
class HouseFeatures(BaseModel):
    size: float
    nb_rooms: int
    garden: bool

class PredictionResponse(BaseModel):
    price: float

class UpdateModelRequest(BaseModel):
    run_id: str

@app.on_event("startup")
def load_initial_model():
    """Loads a model at startup if INITIAL_RUN_ID is set."""
    global model
    initial_run_id = os.getenv("INITIAL_RUN_ID")
    if initial_run_id:
        print(f"Loading initial model from run: {initial_run_id}")
        model = mlflow.pyfunc.load_model(f"runs:/{initial_run_id}/model")

@app.post("/predict", response_model=PredictionResponse)
def predict(features: HouseFeatures):
    if not model:
        raise HTTPException(status_code=503, detail="No model loaded yet.")

    input_df = pd.DataFrame([features.model_dump()])

    input_df['garden'] = input_df['garden'].astype(int)

    prediction = model.predict(input_df)[0]
    return {"price": prediction}

@app.post("/update-model")
def update_model(request: UpdateModelRequest):
    global model
    try:
        print(f"Switching to model from run: {request.run_id}")
        model = mlflow.pyfunc.load_model(f"runs:/{request.run_id}/model")
        return {"status": "success", "current_run_id": request.run_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load model: {str(e)}")
