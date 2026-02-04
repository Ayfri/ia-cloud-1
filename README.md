# House Price Prediction Project

This project provides a simple machine learning pipeline to predict house prices based on size, number of rooms, and the presence of a garden.

## Features
- **Model Training**: Linear regression model trained on house data.
- **FastAPI**: REST API for real-time predictions.
- **Streamlit**: Web interface for interactive predictions.
- **Containerization**: Docker and Docker Compose support.

## Getting Started

### Prerequisites
- Install [UV](https://github.com/astral-sh/uv)

### 1. Installation
Install dependencies using UV:
```bash
uv sync
```

### 2. Train the Model
Run the training script:
```bash
uv run train_model.py
```

### 3. Run the API (FastAPI)
```bash
uv run fast_api.py
```
The API will be available at `http://localhost:8000`. You can test the `/predict` endpoint.

### 4. Run the Web App (Streamlit)
```bash
uv run streamlit run model_app.py
```

## Docker
Build and run the entire stack using Docker Compose:
```bash
docker-compose up --build
```
