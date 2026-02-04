from fastapi import FastAPI


app = FastAPI()


@app.get("/predict")
def predict():
    return {"y_pred": 2}


def main():
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
