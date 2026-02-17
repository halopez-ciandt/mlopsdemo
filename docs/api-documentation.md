# API Documentation

## Overview

The Iris Classification API is a REST API that provides machine learning predictions for classifying iris flowers into three species: Setosa, Versicolor, and Virginica.

## Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: `https://your-render-app.onrender.com`

## Authentication

No authentication required. This is a public demo API.

## Endpoints

### 1. Web Interface

**GET** `/`

Returns the interactive web interface for testing the API.

**Response**: HTML page with form interface

---

### 2. API Information

**GET** `/api`

Returns general information about the API.

**Response:**
```json
{
  "message": "Iris Classification API",
  "version": "1.0.0",
  "description": "MLOps Demo - Classify iris flowers using machine learning",
  "endpoints": {
    "predict": "/predict - Single prediction",
    "predict_batch": "/predict/batch - Batch predictions",
    "health": "/health - Health check",
    "docs": "/docs - API documentation"
  }
}
```

---

### 3. Health Check

**GET** `/health`

Check if the API service and model are healthy.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Model not loaded

---

### 4. Model Information

**GET** `/model/info`

Get information about the loaded machine learning model.

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "features": [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)"
  ],
  "target_classes": ["setosa", "versicolor", "virginica"],
  "n_features": 4,
  "n_classes": 3
}
```

---

### 5. Single Prediction

**POST** `/predict`

Classify a single iris flower based on its measurements.

**Request Body:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Request Schema:**
- `sepal_length` (float, required): Sepal length in cm (0-10)
- `sepal_width` (float, required): Sepal width in cm (0-10)
- `petal_length` (float, required): Petal length in cm (0-10)
- `petal_width` (float, required): Petal width in cm (0-10)

**Response:**
```json
{
  "prediction": "setosa",
  "prediction_id": 0,
  "confidence": 1.0,
  "probabilities": {
    "setosa": 1.0,
    "versicolor": 0.0,
    "virginica": 0.0
  }
}
```

**Status Codes:**
- `200 OK`: Prediction successful
- `422 Unprocessable Entity`: Invalid input data
- `500 Internal Server Error`: Prediction failed

---

### 6. Batch Prediction

**POST** `/predict/batch`

Classify multiple iris flowers in a single request.

**Request Body:**
```json
{
  "samples": [
    {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    },
    {
      "sepal_length": 7.0,
      "sepal_width": 3.2,
      "petal_length": 4.7,
      "petal_width": 1.4
    }
  ]
}
```

**Limitations:**
- Maximum 100 samples per request

**Response:**
```json
{
  "predictions": [
    {
      "prediction": "setosa",
      "prediction_id": 0,
      "confidence": 1.0,
      "probabilities": {
        "setosa": 1.0,
        "versicolor": 0.0,
        "virginica": 0.0
      }
    },
    {
      "prediction": "versicolor",
      "prediction_id": 1,
      "confidence": 0.94,
      "probabilities": {
        "setosa": 0.0,
        "versicolor": 0.94,
        "virginica": 0.06
      }
    }
  ],
  "batch_size": 2
}
```

**Status Codes:**
- `200 OK`: Batch prediction successful
- `400 Bad Request`: Batch size exceeds limit
- `422 Unprocessable Entity`: Invalid input data

---

## Example Usage

### cURL Examples

**Single Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**Batch Prediction:**
```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
      {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
    ]
  }'
```

### Python Examples

```python
import requests

# Single prediction
response = requests.post('http://localhost:8000/predict', json={
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
})

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")

# Batch prediction
batch_response = requests.post('http://localhost:8000/predict/batch', json={
    "samples": [
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
    ]
})

batch_result = batch_response.json()
for i, pred in enumerate(batch_result['predictions']):
    print(f"Sample {i+1}: {pred['prediction']} ({pred['confidence']:.2%})")
```

### JavaScript Examples

```javascript
// Single prediction
const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    sepal_length: 5.1,
    sepal_width: 3.5,
    petal_length: 1.4,
    petal_width: 0.2
  })
});

const result = await response.json();
console.log(`Prediction: ${result.prediction}`);
console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
```

## Error Handling

### Common Error Responses

**422 Unprocessable Entity (Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "sepal_length"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

**400 Bad Request:**
```json
{
  "detail": "Batch size cannot exceed 100 samples"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Prediction failed: Model error details"
}
```

**503 Service Unavailable:**
```json
{
  "detail": "Model not loaded"
}
```

## Rate Limiting

- No rate limiting on free tier
- Recommended: Max 100 requests per minute for optimal performance

## Data Ranges

All measurements should be in centimeters within realistic ranges:

- **Sepal Length**: 4.0 - 8.0 cm (typical range)
- **Sepal Width**: 2.0 - 4.5 cm (typical range)
- **Petal Length**: 1.0 - 7.0 cm (typical range)
- **Petal Width**: 0.1 - 2.5 cm (typical range)

*Note: API accepts values 0-10 cm, but model accuracy is best within typical ranges.*

## Interactive Documentation

Visit `/docs` endpoint for Swagger UI documentation with interactive API testing.

## Model Performance

- **Accuracy**: ~96.7% on test set
- **Model**: Random Forest Classifier
- **Training Data**: Iris flower dataset (150 samples)
- **Classes**: Setosa, Versicolor, Virginica

## Support

For issues or questions:
1. Check the `/health` endpoint
2. Review error messages in API responses
3. Verify input data format and ranges
4. Check the interactive documentation at `/docs`