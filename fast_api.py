from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("output/regression.joblib")

class HouseFeatures(BaseModel):
    size: float
    nb_rooms: int
    garden: bool


@app.post("/predict")
def predict_house(features: HouseFeatures):
    input_data = pd.DataFrame([[features.size, features.nb_rooms, features.garden]], columns=['size', 'nb_rooms', 'garden'])
    price = model.predict(input_data)[0]
    return {"y_pred": price}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
