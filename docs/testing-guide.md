# Testing Guide

This guide covers how to test the Iris Classification MLOps pipeline at all levels.

## Testing Overview

The project includes comprehensive testing at multiple levels:

1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test API endpoints
3. **End-to-End Tests** - Test complete workflows
4. **Performance Tests** - Test under load
5. **Manual Testing** - Interactive testing

---

## Running Tests

### Prerequisites

```bash
# Install test dependencies (included in requirements.txt and requirements-api.txt)
pip install pytest httpx requests

# Ensure model is trained
python3 -m src.models.iris_model
```

### Quick Test Suite

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_iris_model.py -v      # Model tests
pytest tests/test_data_loader.py -v     # Data processing tests
pytest tests/test_api.py -v             # API tests

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Automated Test Script

```bash
# Use the comprehensive test script
./local-test.sh
```

---

## Test Categories

### 1. Model Tests (`tests/test_iris_model.py`)

**What it tests:**
- Model initialization
- Data loading and preprocessing
- Training and prediction functionality
- Model persistence (save/load)
- Evaluation metrics

**Key test cases:**
```python
def test_model_initialization()      # Model setup
def test_load_data()                # Data loading
def test_train_and_predict()        # Core ML functionality
def test_evaluate()                 # Model performance
def test_save_and_load_model()      # Model persistence
def test_main_pipeline()            # Complete training workflow
```

**Run:**
```bash
pytest tests/test_iris_model.py -v
```

### 2. Data Processing Tests (`tests/test_data_loader.py`)

**What it tests:**
- Data loading utilities
- Data preprocessing and normalization
- Data splitting functionality
- Summary statistics generation

**Key test cases:**
```python
def test_load_iris_data()                    # Data loading
def test_load_iris_data_normalized()         # Data normalization
def test_split_data()                        # Train/test splitting
def test_get_data_summary()                  # Data analysis
def test_prepare_data_pipeline()             # Complete data pipeline
```

**Run:**
```bash
pytest tests/test_data_loader.py -v
```

### 3. API Tests (`tests/test_api.py`)

**What it tests:**
- All API endpoints
- Request/response validation
- Error handling
- Performance and consistency

**Key test cases:**
```python
def test_health_check_endpoint()         # Health checks
def test_model_info_endpoint()           # Model metadata
def test_single_prediction_valid_input() # Single predictions
def test_batch_prediction_valid_input()  # Batch predictions
def test_prediction_consistency()        # Consistency checks
def test_api_documentation_endpoints()   # Documentation
```

**Run:**
```bash
pytest tests/test_api.py -v
```

---

## Manual Testing

### 1. Interactive API Testing Script

```bash
# Start the API server
python3 -m uvicorn src.api.app:app --reload

# In another terminal, run the test script
python3 test-api.py
```

**Expected Output:**
```
🚀 Starting API Tests
==================================================
🏥 Testing health endpoint...
Status: 200
Response: {'status': 'healthy', 'model_loaded': True, 'timestamp': '2024-01-01T00:00:00Z'}

📊 Testing model info endpoint...
Status: 200
Model type: RandomForestClassifier
Features: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
Classes: ['setosa', 'versicolor', 'virginica']

🔮 Testing single prediction...
Status: 200
Prediction: setosa
Confidence: 1.0000
Probabilities: {'setosa': 1.0, 'versicolor': 0.0, 'virginica': 0.0}

📦 Testing batch prediction...
Status: 200
Batch size: 3
  Sample 1: setosa (confidence: 1.0000)
  Sample 2: versicolor (confidence: 0.9403)
  Sample 3: virginica (confidence: 0.9969)

==================================================
📈 Results: 4/4 tests passed
✅ All tests passed! API is working correctly.
```

### 2. Web Interface Testing

1. **Start server:** `python3 -m uvicorn src.api.app:app --reload`
2. **Open browser:** `http://localhost:8000`
3. **Test scenarios:**
   - Use pre-filled examples for each species
   - Try custom values
   - Test form validation (negative values, missing fields)
   - Check probability visualizations

### 3. cURL Testing

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model/info

# Single prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'

# Batch prediction
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
      {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
    ]
  }'
```

---

## Performance Testing

### Load Testing with Python

```python
import asyncio
import aiohttp
import time

async def test_prediction(session, data):
    async with session.post('http://localhost:8000/predict', json=data) as response:
        return await response.json()

async def load_test(num_requests=100):
    test_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    async with aiohttp.ClientSession() as session:
        start_time = time.time()

        tasks = [test_prediction(session, test_data) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

        end_time = time.time()

        print(f"Completed {num_requests} requests in {end_time - start_time:.2f} seconds")
        print(f"Average response time: {(end_time - start_time) / num_requests * 1000:.2f}ms")

        # Check all predictions are consistent
        predictions = [r['prediction'] for r in responses]
        print(f"Prediction consistency: {len(set(predictions))} unique predictions")

# Run load test
asyncio.run(load_test(50))
```

### Stress Testing

```bash
# Using Apache Bench (if installed)
ab -n 100 -c 10 -p test_data.json -T application/json http://localhost:8000/predict

# Using curl in a loop
for i in {1..20}; do
  time curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}' \
    > /dev/null 2>&1 &
done
wait
```

---

## Continuous Integration Testing

### GitHub Actions Workflow

The CI pipeline automatically runs:

1. **Code Quality:**
   ```yaml
   - name: Lint with flake8
   - name: Format check with black
   - name: Type check with mypy
   ```

2. **Unit Tests:**
   ```yaml
   - name: Test with pytest
     run: pytest tests/ -v --tb=short
   ```

3. **Model Training:**
   ```yaml
   - name: Train model
     run: python3 -m src.models.iris_model
   ```

4. **Model Validation:**
   ```yaml
   - name: Validate model performance
     run: |
       python3 -c "
       # Model validation script
       "
   ```

### Running CI Tests Locally

```bash
# Simulate CI environment
python3 -m venv ci_env
source ci_env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt

# Run CI test sequence
black --check src tests
flake8 src tests --max-line-length=88 --extend-ignore=E203,W503
mypy src --ignore-missing-imports
pytest tests/ -v --tb=short
python3 -m src.models.iris_model

# API-specific CI tests
pytest tests/test_api.py -v
```

---

## Test Data and Scenarios

### Test Cases for Each Iris Species

**Setosa (Class 0):**
```json
{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
{"sepal_length": 4.9, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.2}
{"sepal_length": 5.4, "sepal_width": 3.9, "petal_length": 1.7, "petal_width": 0.4}
```

**Versicolor (Class 1):**
```json
{"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
{"sepal_length": 6.4, "sepal_width": 3.2, "petal_length": 4.5, "petal_width": 1.5}
{"sepal_length": 5.7, "sepal_width": 2.8, "petal_length": 4.5, "petal_width": 1.3}
```

**Virginica (Class 2):**
```json
{"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 6.0, "petal_width": 2.5}
{"sepal_length": 7.1, "sepal_width": 3.0, "petal_length": 5.9, "petal_width": 2.1}
{"sepal_length": 6.5, "sepal_width": 3.0, "petal_length": 5.8, "petal_width": 2.2}
```

### Edge Cases

**Boundary Values:**
```json
{"sepal_length": 0.0, "sepal_width": 0.0, "petal_length": 0.0, "petal_width": 0.0}
{"sepal_length": 10.0, "sepal_width": 10.0, "petal_length": 10.0, "petal_width": 10.0}
```

**Invalid Inputs:**
```json
{"sepal_length": -1.0, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}
{"sepal_length": 5.1, "sepal_width": 15.0, "petal_length": 1.4, "petal_width": 0.2}
```

**Missing Fields:**
```json
{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4}
{}
```

---

## Debugging Failed Tests

### Common Test Failures

**1. Model not found:**
```
FileNotFoundError: Model file not found
Solution: Run `python3 -m src.models.iris_model` to train model
```

**2. Import errors:**
```
ModuleNotFoundError: No module named 'src'
Solution: Ensure PYTHONPATH includes project root
```

**3. API connection errors:**
```
ConnectionError: Failed to connect to localhost:8000
Solution: Start API server before running API tests
```

### Debug Commands

```bash
# Check model file exists
ls -la models/iris_model.joblib

# Test model loading
python3 -c "import joblib; model = joblib.load('models/iris_model.joblib'); print('Model loaded successfully')"

# Test imports
python3 -c "from src.models.iris_model import IrisModel; print('Import successful')"
python3 -c "from src.api.app import app; print('API import successful')"

# Check API server
curl -f http://localhost:8000/health || echo "API server not running"
```

### Verbose Testing

```bash
# Maximum verbosity
pytest tests/ -vvv --tb=long --show-capture=all

# Test specific function
pytest tests/test_api.py::TestAPIEndpoints::test_single_prediction_valid_input -v

# Print outputs
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x
```

---

## Test Coverage

### Generate Coverage Reports

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

### Target Coverage Goals

- **Overall Coverage**: >90%
- **Critical Paths**: 100% (model prediction, API endpoints)
- **Error Handling**: >80%
- **Edge Cases**: >70%

---

## Testing Best Practices

### 1. Test Structure

```python
class TestComponent:
    """Test cases for Component."""

    def setup_method(self):
        """Set up test fixtures."""
        pass

    def test_functionality_description(self):
        """Test specific functionality with clear description."""
        # Arrange
        input_data = {...}

        # Act
        result = function_under_test(input_data)

        # Assert
        assert expected_condition
```

### 2. Naming Conventions

- Test files: `test_*.py`
- Test classes: `TestComponentName`
- Test methods: `test_functionality_description`

### 3. Test Data Management

- Use fixtures for reusable test data
- Separate test data from test logic
- Include edge cases and error scenarios

### 4. Assertion Best Practices

```python
# Good - Specific assertions
assert response.status_code == 200
assert "prediction" in result
assert 0.0 <= result["confidence"] <= 1.0

# Bad - Vague assertions
assert response.ok
assert result
```

---

## Production Testing

### Pre-deployment Checklist

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Load testing completed
- [ ] Security scanning passed
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Health checks working

### Post-deployment Testing

1. **Smoke Tests:**
   ```bash
   # Test deployed API
   curl https://your-app.onrender.com/health
   curl https://your-app.onrender.com/model/info
   ```

2. **End-to-End Tests:**
   ```bash
   # Run full test suite against deployed API
   API_BASE_URL=https://your-app.onrender.com python3 test-api.py
   ```

3. **Monitoring Setup:**
   - Health check monitoring
   - Error rate monitoring
   - Performance monitoring

Remember: **Test early, test often, test thoroughly!** 🧪✅