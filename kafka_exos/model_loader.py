import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "output" / "regression.joblib"

def load_model():
    try:
        model = joblib.load(str(MODEL_PATH))
        print(f"Model loaded from {MODEL_PATH}")
        return model
    except FileNotFoundError:
        print(f"Error: Model not found at {MODEL_PATH}")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def predict(model, input_data):
    if model is None:
        return None
    try:
        return model.predict(input_data)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

if __name__ == "__main__":
    model = load_model()
    if model:
        test_data = [[1500, 3, 1]]
        prediction = predict(model, test_data)
        print(f"Prediction: {prediction}")
