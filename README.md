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

## Kafka Workflows

### Setup: Create Partitions
Initialize Kafka partitions for both input and output topics:
```bash
uv run -m kafka_exos.create_partitions
```
This creates 2 partitions per topic to enable parallel processing and prevent duplicate message handling.

### Workflow 1: Single Message Production & Consumption
**Purpose**: Test basic producer-consumer interaction with partition routing.

1. Start consumer (partition 0):
```bash
uv run -m kafka_exos.consumer 0
```

2. Send message:
```bash
uv run -m kafka_exos.producer
```

3. Verify message received on assigned partition.

---

### Workflow 2: ML Model Predictions (Full Pipeline)

**Purpose**: Production ML inference pipeline - predictions should be processed only once across multiple consumers.

#### Step 1: Start Prediction Consumers
Each consumer handles one partition independently:

Terminal 1 (partition 0):
```bash
uv run -m kafka_exos.consumer_predict 0
```

Terminal 2 (partition 1):
```bash
uv run -m kafka_exos.consumer_predict 1
```

**What they do**:
- Load ML model at startup
- Listen on their assigned partition
- Receive raw input data
- Run predictions using the trained model
- Send results to `OUTPUT_TOPIC`

#### Step 2 (Optional): Monitor Predictions
View prediction results:

Terminal 3 (partition 0):
```bash
uv run -m kafka_exos.consumer_view_predictions 0
```

Terminal 4 (partition 1):
```bash
uv run -m kafka_exos.consumer_view_predictions 1
```

#### Step 3: Send Data for Prediction
Send multiple messages (they route to random partitions):
```bash
uv run -m kafka_exos.producer_multi 5
```

**Result**:
- Each message goes to partition 0 or 1 randomly
- Only the corresponding consumer receives and processes it
- Predictions are made and sent to `OUTPUT_TOPIC`
- No duplicate processing even with multiple consumers
- Enables horizontal scaling of prediction workers

---

## Architecture Overview

```
Producer (random partition)
    ↓
Input Topic [Partition 0, Partition 1]
    ↓
Consumer Predict 0 ─→ Load Model ─→ Predict ─→ Output Topic [Partition 0]
Consumer Predict 1 ─→ Load Model ─→ Predict ─→ Output Topic [Partition 1]
    ↓
Consumer View (optional monitoring)
```

## Docker
Build and run the entire stack using Docker Compose:
```bash
docker-compose up --build
```
