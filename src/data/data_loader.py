"""
Data loading and preprocessing utilities for MLOps demo.
"""
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import logging
from typing import Dict, Any, Tuple, List
import numpy.typing as npt

logger = logging.getLogger(__name__)


class DataLoader:
    """Data loading and preprocessing utilities."""

    def __init__(self) -> None:
        """Initialize data loader."""
        self.scaler = StandardScaler()
        self.feature_names = None
        self.target_names = None

    def load_iris_data(self, normalize: bool = False) -> Dict[str, Any]:
        """
        Load Iris dataset.

        Args:
            normalize (bool): Whether to normalize features

        Returns:
            dict: Dictionary containing features, target, and metadata
        """
        logger.info("Loading Iris dataset...")

        iris = load_iris()

        # Store metadata
        self.feature_names = iris.feature_names
        self.target_names = iris.target_names

        # Create feature matrix and target vector
        X = iris.data
        y = iris.target

        # Optional normalization
        if normalize:
            logger.info("Normalizing features...")
            X = self.scaler.fit_transform(X)

        logger.info(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")

        return {
            "features": X,
            "target": y,
            "feature_names": self.feature_names,
            "target_names": self.target_names,
            "normalized": normalize,
        }

    def split_data(
        self, X: Any, y: Any, test_size: float = 0.2, random_state: int = 42
    ) -> Any:
        """
        Split data into training and testing sets.

        Args:
            X: Features
            y: Target
            test_size (float): Proportion of test data
            random_state (int): Random seed

        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        logger.info(f"Splitting data with test_size={test_size}")

        return train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y,  # Ensure balanced split
        )

    def get_data_summary(self, X: Any, y: Any) -> Dict[str, Any]:
        """
        Get summary statistics of the dataset.

        Args:
            X: Features
            y: Target

        Returns:
            dict: Summary statistics
        """
        if not hasattr(X, "shape"):
            X = np.array(X)
        if not hasattr(y, "shape"):
            y = np.array(y)

        summary = {
            "n_samples": X.shape[0],
            "n_features": X.shape[1] if len(X.shape) > 1 else 1,
            "n_classes": len(np.unique(y)),
            "class_distribution": dict(zip(*np.unique(y, return_counts=True))),
            "feature_stats": {
                "mean": np.mean(X, axis=0).tolist()
                if len(X.shape) > 1
                else [np.mean(X)],
                "std": np.std(X, axis=0).tolist() if len(X.shape) > 1 else [np.std(X)],
            },
        }

        return summary


def prepare_data_pipeline(
    normalize: bool = False, test_size: float = 0.2, random_state: int = 42
) -> Dict[str, Any]:
    """
    Complete data preparation pipeline.

    Args:
        normalize (bool): Whether to normalize features
        test_size (float): Test set proportion
        random_state (int): Random seed

    Returns:
        dict: Complete dataset splits and metadata
    """
    loader = DataLoader()

    # Load data
    data = loader.load_iris_data(normalize=normalize)

    # Split data
    X_train, X_test, y_train, y_test = loader.split_data(
        data["features"], data["target"], test_size=test_size, random_state=random_state
    )

    # Get summaries
    train_summary = loader.get_data_summary(X_train, y_train)
    test_summary = loader.get_data_summary(X_test, y_test)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": data["feature_names"],
        "target_names": data["target_names"],
        "train_summary": train_summary,
        "test_summary": test_summary,
        "normalized": normalize,
    }
