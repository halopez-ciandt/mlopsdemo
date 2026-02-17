# MLOps Demo Project

🌸 **Complete MLOps Pipeline for Iris Classification with FastAPI Web Service**

A production-ready MLOps demonstration featuring machine learning model development, comprehensive testing, CI/CD automation, and cloud deployment.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 Live Demo

- **Web Interface**: [Try the Interactive Demo](https://iris-classification-api.onrender.com) *(Deploy first)*
- **API Documentation**: [Swagger UI Docs](https://iris-classification-api.onrender.com/docs)
- **Health Check**: [API Status](https://iris-classification-api.onrender.com/health)

## ✨ Features

### 🤖 Machine Learning
- **Model**: Random Forest Classifier (96.7% accuracy)
- **Dataset**: Iris flower classification (3 species)
- **Preprocessing**: Automated data loading and normalization
- **Validation**: Comprehensive model evaluation and testing

### 🌐 Web API
- **FastAPI**: Modern, fast REST API framework
- **Interactive UI**: Beautiful web interface for testing
- **Batch Processing**: Support for single and batch predictions
- **Documentation**: Auto-generated API docs with Swagger UI

### 🧪 Testing & Quality
- **Unit Tests**: Comprehensive test suite (15+ test cases)
- **API Tests**: Full endpoint testing with FastAPI TestClient
- **Code Quality**: Black formatting, flake8 linting, mypy type checking
- **CI/CD**: Automated testing and deployment pipelines

### 🚀 Deployment Ready
- **Multiple Platforms**: Render, Railway, Fly.io, Docker
- **Production Config**: Health checks, error handling, monitoring
- **Documentation**: Complete API docs and deployment guides

## 📋 Quick Start

### 1. Local Development

```bash
# Clone repository
git clone https://github.com/halopez-ciandt/mlopsdemo.git
cd mlopsdemo

# Setup environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements-api.txt

# Train model and start API
python3 -m src.models.iris_model
python3 -m uvicorn src.api.app:app --reload

# Visit: http://localhost:8000
```

### 2. Run Tests

```bash
# Quick test script
./local-test.sh

# Or run manually
pytest tests/ -v
python3 test-api.py
```

### 3. Deploy to Cloud

**Render (Recommended - Free):**
1. Fork this repository
2. Sign up at [render.com](https://render.com)
3. Create "New Web Service" → Connect GitHub → Deploy!
4. Render will use `render.yaml` automatically

**Other platforms:** See [Deployment Guide](docs/deployment-guide.md)

## 🏗️ Project Structure

```
├── src/
│   ├── api/
│   │   ├── app.py              # FastAPI application
│   │   └── __init__.py
│   ├── models/
│   │   ├── iris_model.py       # ML model implementation
│   │   └── __init__.py
│   └── data/
│       ├── data_loader.py      # Data processing utilities
│       └── __init__.py
├── tests/
│   ├── test_api.py             # API endpoint tests
│   ├── test_iris_model.py      # Model unit tests
│   └── test_data_loader.py     # Data processing tests
├── docs/
│   ├── api-documentation.md    # Complete API reference
│   ├── deployment-guide.md     # Deployment instructions
│   ├── testing-guide.md        # Testing documentation
│   └── mlops-plan.md          # Original project plan
├── static/
│   └── index.html              # Interactive web interface
├── .github/workflows/
│   ├── ci.yml                  # CI/CD pipeline
│   └── model-deployment.yml    # Deployment automation
├── render.yaml                 # Render.com deployment config
├── Dockerfile                  # Docker container config
├── requirements-api.txt        # API dependencies
└── test-api.py                # API testing script
```

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **ML Framework** | scikit-learn, pandas, numpy | Model training and data processing |
| **API Framework** | FastAPI, Uvicorn | REST API and web service |
| **Frontend** | HTML/CSS/JavaScript | Interactive web interface |
| **Testing** | pytest, httpx | Unit and integration testing |
| **Code Quality** | black, flake8, mypy | Code formatting and linting |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Deployment** | Render, Docker, Railway | Cloud hosting platforms |
| **Monitoring** | Built-in health checks | Service monitoring |

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Interactive web interface |
| `GET` | `/docs` | API documentation (Swagger UI) |
| `GET` | `/health` | Health check and service status |
| `GET` | `/model/info` | Model metadata and information |
| `POST` | `/predict` | Single flower classification |
| `POST` | `/predict/batch` | Batch predictions (up to 100 samples) |

### Example Usage

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
# Output: Prediction: setosa, Confidence: 100.00%
```

```bash
# cURL example
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## 🧪 Testing

### Automated Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_api.py -v           # API tests
pytest tests/test_iris_model.py -v    # Model tests
pytest tests/test_data_loader.py -v   # Data tests

# Test with coverage
pytest tests/ --cov=src --cov-report=html
```

### Manual Testing

```bash
# Interactive API testing
python3 test-api.py

# Web interface testing
# Visit http://localhost:8000 in browser
```

**Test Coverage:**
- ✅ 15+ comprehensive test cases
- ✅ API endpoint validation
- ✅ Model functionality testing
- ✅ Error handling verification
- ✅ Performance and consistency checks

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [API Documentation](docs/api-documentation.md) | Complete REST API reference |
| [Deployment Guide](docs/deployment-guide.md) | Cloud deployment instructions |
| [Testing Guide](docs/testing-guide.md) | Comprehensive testing documentation |
| [Original MLOps Plan](docs/mlops-plan.md) | Project planning and architecture |

## 🚀 CI/CD Pipeline

### GitHub Actions Workflows

**Continuous Integration (`.github/workflows/ci.yml`):**
- ✅ Multi-Python version testing (3.9, 3.10, 3.11)
- ✅ Code quality checks (black, flake8, mypy)
- ✅ Comprehensive test suite
- ✅ Automated model training
- ✅ Security scanning

**Deployment Pipeline (`.github/workflows/model-deployment.yml`):**
- ✅ Staging deployment automation
- ✅ Production deployment with manual approval
- ✅ Health checks and validation
- ✅ Rollback capabilities

## 🌍 Deployment Options

### Free Tier Platforms

| Platform | Free Allowance | Deployment |
|----------|----------------|------------|
| **🔗 Render** | 750 hours/month | [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy) |
| **🚂 Railway** | $5 credit/month | [Deploy to Railway](https://railway.app/new/template) |
| **🪰 Fly.io** | 3 apps, 256MB | `flyctl deploy` |
| **🐳 Docker** | Self-hosted | `docker build -t iris-api .` |

**Recommended:** Render for easiest deployment with automatic `render.yaml` detection.

## 🔍 Monitoring & Health

### Health Check Endpoints

```bash
# Service health
curl https://your-app.onrender.com/health

# Model information
curl https://your-app.onrender.com/model/info
```

### Built-in Monitoring

- ✅ **Health Checks**: Automatic service health monitoring
- ✅ **Model Validation**: Startup model loading verification
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **Logging**: Structured logging for debugging
- ✅ **Performance Tracking**: Request/response monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Run the test suite (`pytest tests/ -v`)
5. Commit using conventional commits (`git commit -m "feat: add amazing feature"`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Iris Dataset**: Ronald Fisher's classic dataset
- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning library
- **Render**: Free hosting platform
- **GitHub Actions**: CI/CD automation

---

**🎯 Perfect for learning MLOps, API development, and cloud deployment!**

⭐ **Star this repository if it helped you!** ⭐