"""
Unit tests for Iris model.
"""
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import tempfile
import os

from src.models.iris_model import IrisModel


class TestIrisModel:
    """Test cases for IrisModel class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.model = IrisModel(random_state=42)

    def test_model_initialization(self):
        """Test model initialization."""
        assert self.model.model is not None
        assert self.model.feature_names is None
        assert self.model.target_names is None

    def test_load_data(self):
        """Test data loading."""
        data = self.model.load_data()

        # Check data structure
        assert isinstance(data, pd.DataFrame)
        assert data.shape[0] == 150  # Iris has 150 samples
        assert data.shape[1] == 5  # 4 features + 1 target
        assert "target" in data.columns

        # Check feature and target names are set
        assert self.model.feature_names is not None
        assert self.model.target_names is not None
        assert len(self.model.feature_names) == 4
        assert len(self.model.target_names) == 3

    def test_train_and_predict(self):
        """Test model training and prediction."""
        # Load data
        data = self.model.load_data()
        X = data.drop("target", axis=1)
        y = data["target"]

        # Train model
        self.model.train(X, y)

        # Make predictions
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        # Check predictions
        assert len(predictions) == len(y)
        assert all(pred in [0, 1, 2] for pred in predictions)

        # Check probabilities
        assert probabilities.shape == (len(y), 3)  # 3 classes
        assert np.allclose(probabilities.sum(axis=1), 1.0)  # Probabilities sum to 1

    def test_evaluate(self):
        """Test model evaluation."""
        # Load and prepare data
        data = self.model.load_data()
        X = data.drop("target", axis=1)
        y = data["target"]

        # Train model
        self.model.train(X, y)

        # Evaluate
        metrics = self.model.evaluate(X, y)

        # Check metrics structure
        assert "accuracy" in metrics
        assert "classification_report" in metrics
        assert "confusion_matrix" in metrics

        # Check accuracy is reasonable
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert metrics["accuracy"] > 0.8  # Should be high on training data

    def test_save_and_load_model(self):
        """Test model saving and loading."""
        # Train a model
        data = self.model.load_data()
        X = data.drop("target", axis=1)
        y = data["target"]
        self.model.train(X, y)

        # Get predictions before saving
        predictions_before = self.model.predict(X)

        # Save model to temporary file
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, "test_model.joblib")
            self.model.save_model(model_path)

            # Check file was created
            assert Path(model_path).exists()

            # Load model into new instance
            new_model = IrisModel()
            new_model.load_model(model_path)

            # Get predictions after loading
            predictions_after = new_model.predict(X)

            # Check predictions are the same
            np.testing.assert_array_equal(predictions_before, predictions_after)

    def test_main_pipeline(self):
        """Test the main training pipeline."""
        from src.models.iris_model import main

        # Run main pipeline
        metrics = main()

        # Check that metrics are returned
        assert isinstance(metrics, dict)
        assert "accuracy" in metrics
        assert metrics["accuracy"] > 0.0

        # Check that model file was created
        model_path = Path("models/iris_model.joblib")
        assert model_path.exists()

        # Clean up
        if model_path.exists():
            model_path.unlink()
        if model_path.parent.exists() and not any(model_path.parent.iterdir()):
            model_path.parent.rmdir()
