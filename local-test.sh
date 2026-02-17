#!/bin/bash
# Local testing script for MLOps demo

set -e  # Exit on any error

echo "🚀 MLOps Demo - Local Testing Script"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Run code quality checks
echo "🔍 Running code quality checks..."
echo "  - Formatting with black..."
black src tests

echo "  - Linting with flake8..."
flake8 src tests --max-line-length=88 --extend-ignore=E203,W503 || echo "⚠️ Some linting warnings found"

echo "  - Type checking with mypy..."
mypy src --ignore-missing-imports || echo "⚠️ Some type checking warnings found"

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v

# Train model
echo "🤖 Training model..."
python3 -m src.models.iris_model

# Quick model test
echo "🎯 Testing model predictions..."
python3 -c "
from src.models.iris_model import IrisModel
import numpy as np

model = IrisModel()
data = model.load_data()
X = data.drop('target', axis=1)
y = data['target']

model.train(X, y)
metrics = model.evaluate(X, y)

print(f'✅ Model trained successfully!')
print(f'   Accuracy: {metrics[\"accuracy\"]:.4f}')

# Test prediction
test_sample = np.array([[5.1, 3.5, 1.4, 0.2]])
prediction = model.predict(test_sample)
probabilities = model.predict_proba(test_sample)

print(f'   Test prediction: {prediction[0]} ({model.target_names[prediction[0]]})')
print(f'   Confidence: {max(probabilities[0]):.4f}')
"

echo ""
echo "✅ All local tests completed successfully!"
echo "🎉 MLOps demo is ready for deployment!"