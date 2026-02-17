#!/usr/bin/env python3
"""
Local API testing script
"""
import requests
import json
import time
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n🔮 Testing single prediction...")

    test_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print(f"Probabilities: {result['probabilities']}")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Single prediction failed: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n📦 Testing batch prediction...")

    batch_data = {
        "samples": [
            {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
            {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4},
            {"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 6.0, "petal_width": 2.5}
        ]
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/predict/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Batch size: {result['batch_size']}")

        for i, pred in enumerate(result['predictions']):
            print(f"  Sample {i+1}: {pred['prediction']} (confidence: {pred['confidence']:.4f})")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Batch prediction failed: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n📊 Testing model info endpoint...")

    try:
        response = requests.get(f"{API_BASE_URL}/model/info")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Model type: {result['model_type']}")
        print(f"Features: {result['features']}")
        print(f"Classes: {result['target_classes']}")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Model info failed: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Starting API Tests")
    print("=" * 50)

    # Wait a bit for server to start
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)

    tests = [
        test_health,
        test_model_info,
        test_single_prediction,
        test_batch_prediction
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        time.sleep(1)

    print(f"\n{'='*50}")
    print(f"📈 Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All tests passed! API is working correctly.")
        print(f"🌐 Visit {API_BASE_URL} to try the web interface")
        print(f"📚 API docs available at {API_BASE_URL}/docs")
    else:
        print("❌ Some tests failed. Check the server logs.")

    return passed == total

if __name__ == "__main__":
    main()