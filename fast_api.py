from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class HouseFeatures(BaseModel):
    size: float
    nb_rooms: int
    garden: bool


@app.post("/predict")
def predict_house(features: HouseFeatures):
    price = features.size * 1000 + features.nb_rooms * 5000
    return {"y_pred": price}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
