# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

End-to-end MLOps pipeline demo: scikit-learn Iris classification model → CI/CD → Azure ML Services deployment. Currently in Phase 1 (foundation) — model and data loading exist, but no tests, CI/CD, or cloud infrastructure yet.

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Does not exist yet — create when adding dependencies
```

Python 3.9+ required. Node 22 specified in `.nvmrc` (likely for tooling, not core ML code).

## Commands

No build system, test suite, or linting is configured yet. When added, the plan calls for:

- **Testing**: `pytest`
- **Formatting**: `black .`
- **Linting**: `flake8`
- **Type checking**: `mypy`
- **Training**: `python src/models/iris_model.py`

## Architecture

```
src/
  models/iris_model.py   — IrisModel class (RandomForestClassifier, train/evaluate/save/load)
  data/data_loader.py    — DataLoader class + prepare_data_pipeline() convenience function
  utils/                 — Empty, placeholder for helpers
```

**Key patterns:**
- `IrisModel` handles its own data loading via `load_data()` (loads sklearn's iris dataset directly)
- `DataLoader` is a separate abstraction with normalization and splitting — not yet integrated with `IrisModel`
- Models are serialized with `joblib` to `models/` directory
- Both modules use Python `logging` for output

## Planned Phases (from docs/mlops-plan.md)

1. **Foundation** — ML model, data pipeline, tests, dependencies *(in progress)*
2. **MLOps Infrastructure** — GitHub Actions CI/CD, MLflow experiment tracking, model validation
3. **Azure ML Integration** — workspace setup, model registration, managed endpoints, blue/green deploys
4. **Monitoring** — drift detection, automated retraining, alerting, dashboards

Target stack: GitHub Actions, Docker, Azure ML Services, Azure Container Registry, MLflow.
