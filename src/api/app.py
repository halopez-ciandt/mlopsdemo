"""
FastAPI application for serving the Iris classification model.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Iris Classification API",
    description="MLOps Demo - Iris flower classification using Random Forest",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    # Static directory might not exist in some deployments
    pass


# Pydantic models for request/response
class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=0, le=10, description="Sepal length in cm")
    sepal_width: float = Field(..., ge=0, le=10, description="Sepal width in cm")
    petal_length: float = Field(..., ge=0, le=10, description="Petal length in cm")
    petal_width: float = Field(..., ge=0, le=10, description="Petal width in cm")

    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        }


class BatchIrisFeatures(BaseModel):
    samples: List[IrisFeatures]


class PredictionResponse(BaseModel):
    prediction: str
    prediction_id: int
    confidence: float
    probabilities: Dict[str, float]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    batch_size: int


# Global model variable
model = None
feature_names = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
]
target_names = ["setosa", "versicolor", "virginica"]


def load_model() -> None:
    """Load the trained model from file."""
    global model

    # Try different possible paths
    model_paths = [
        "models/iris_model.joblib",
        "/app/models/iris_model.joblib",
        "iris_model.joblib",
    ]

    for model_path in model_paths:
        if Path(model_path).exists():
            try:
                model = joblib.load(model_path)
                logger.info(f"Model loaded successfully from {model_path}")
                return
            except Exception as e:
                logger.warning(f"Failed to load model from {model_path}: {e}")
                continue

    # If no pre-trained model found, train a new one
    logger.warning("No pre-trained model found. Training new model...")
    try:
        from src.models.iris_model import IrisModel

        iris_model = IrisModel()
        data = iris_model.load_data()
        X = data.drop("target", axis=1)
        y = data["target"]
        iris_model.train(X, y)

        # Save the model
        os.makedirs("models", exist_ok=True)
        iris_model.save_model("models/iris_model.joblib")
        model = iris_model.model
        logger.info("New model trained and loaded successfully")

    except Exception as e:
        logger.error(f"Failed to train new model: {e}")
        raise RuntimeError("Could not load or train model")


@app.on_event("startup")
async def startup_event() -> None:
    """Load model on startup."""
    load_model()


@app.get("/")
async def root() -> Any:
    """Serve the web interface."""
    try:
        return FileResponse("static/index.html")
    except FileNotFoundError:
        return {
            "message": "Iris Classification API",
            "version": "1.0.0",
            "description": "MLOps Demo - Classify iris flowers using machine learning",
            "endpoints": {
                "predict": "/predict - Single prediction",
                "predict_batch": "/predict/batch - Batch predictions",
                "health": "/health - Health check",
                "docs": "/docs - API documentation",
            },
        }


@app.get("/api")
async def api_info() -> Dict[str, Any]:
    """API information endpoint."""
    return {
        "message": "Iris Classification API",
        "version": "1.0.0",
        "description": "MLOps Demo - Classify iris flowers using machine learning",
        "endpoints": {
            "predict": "/predict - Single prediction",
            "predict_batch": "/predict/batch - Batch predictions",
            "health": "/health - Health check",
            "docs": "/docs - API documentation",
        },
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": "2024-01-01T00:00:00Z",
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: IrisFeatures) -> PredictionResponse:
    """Make a single prediction."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert features to numpy array
        feature_array = np.array(
            [
                [
                    features.sepal_length,
                    features.sepal_width,
                    features.petal_length,
                    features.petal_width,
                ]
            ]
        )

        # Make prediction
        prediction_id = int(model.predict(feature_array)[0])
        prediction_name = target_names[prediction_id]

        # Get probabilities
        probabilities = model.predict_proba(feature_array)[0]
        confidence = float(max(probabilities))

        prob_dict = {
            name: float(prob) for name, prob in zip(target_names, probabilities)
        }

        return PredictionResponse(
            prediction=prediction_name,
            prediction_id=prediction_id,
            confidence=confidence,
            probabilities=prob_dict,
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(batch: BatchIrisFeatures) -> BatchPredictionResponse:
    """Make batch predictions."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if len(batch.samples) > 100:
        raise HTTPException(
            status_code=400, detail="Batch size cannot exceed 100 samples"
        )

    try:
        predictions = []

        for sample in batch.samples:
            # Convert features to numpy array
            feature_array = np.array(
                [
                    [
                        sample.sepal_length,
                        sample.sepal_width,
                        sample.petal_length,
                        sample.petal_width,
                    ]
                ]
            )

            # Make prediction
            prediction_id = int(model.predict(feature_array)[0])
            prediction_name = target_names[prediction_id]

            # Get probabilities
            probabilities = model.predict_proba(feature_array)[0]
            confidence = float(max(probabilities))

            prob_dict = {
                name: float(prob) for name, prob in zip(target_names, probabilities)
            }

            predictions.append(
                PredictionResponse(
                    prediction=prediction_name,
                    prediction_id=prediction_id,
                    confidence=confidence,
                    probabilities=prob_dict,
                )
            )

        return BatchPredictionResponse(
            predictions=predictions, batch_size=len(predictions)
        )

    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/model/info")
async def model_info() -> Dict[str, Any]:
    """Get model information."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "model_type": "RandomForestClassifier",
        "features": feature_names,
        "target_classes": target_names,
        "n_features": len(feature_names),
        "n_classes": len(target_names),
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
