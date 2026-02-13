# MLOps Demo Project

A complete end-to-end MLOps pipeline demonstration that takes a simple machine learning model through development, CI/CD, and production deployment on Azure ML Services.

## Overview

This project demonstrates a production-ready MLOps workflow including:
- Simple ML model implementation (scikit-learn)
- Automated CI/CD pipeline with GitHub Actions
- Model versioning and artifact management
- Azure ML Services deployment
- Production monitoring and management

## Quick Start

1. **View the Plan**: See `docs/mlops-plan.md` for the complete implementation roadmap
2. **Prerequisites**: Azure subscription, Python 3.9+, Azure CLI
3. **Setup**: Create virtual environment and install dependencies
4. **Deploy**: Follow the phase-by-phase implementation guide

## Project Structure

```
├── src/                 # Source code
│   ├── models/         # ML model implementations
│   ├── data/           # Data processing utilities
│   └── utils/          # Helper functions
├── tests/              # Test suite
├── data/               # Sample datasets
├── notebooks/          # Jupyter notebooks for exploration
├── docs/               # Documentation
│   └── mlops-plan.md   # Complete implementation plan
└── .github/workflows/  # CI/CD pipelines
```

## Technology Stack

- **ML Framework**: scikit-learn, pandas, numpy
- **CI/CD**: GitHub Actions, Docker
- **Cloud**: Azure ML Services, Azure Container Registry
- **Monitoring**: MLflow, Azure Monitor
- **Testing**: pytest, black, flake8

## Implementation Phases

1. **Foundation**: Basic ML model and project structure
2. **MLOps Infrastructure**: CI/CD automation and model management
3. **Azure Integration**: Cloud deployment and serving
4. **Monitoring**: Production monitoring and operations

## Getting Started

```bash
# Clone and setup
git clone <repo-url>
cd mlopsdemo
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Follow the detailed plan in docs/mlops-plan.md
```