"""
Unit tests for data loader.
"""
import pytest
import numpy as np
from src.data.data_loader import DataLoader, prepare_data_pipeline


class TestDataLoader:
    """Test cases for DataLoader class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.loader = DataLoader()

    def test_load_iris_data(self):
        """Test Iris data loading."""
        data = self.loader.load_iris_data()

        # Check data structure
        assert 'features' in data
        assert 'target' in data
        assert 'feature_names' in data
        assert 'target_names' in data

        # Check dimensions
        assert data['features'].shape == (150, 4)
        assert data['target'].shape == (150,)
        assert len(data['feature_names']) == 4
        assert len(data['target_names']) == 3

        # Check normalization flag
        assert data['normalized'] == False

    def test_load_iris_data_normalized(self):
        """Test Iris data loading with normalization."""
        data = self.loader.load_iris_data(normalize=True)

        # Check that features are normalized (mean ≈ 0, std ≈ 1)
        features = data['features']
        means = np.mean(features, axis=0)
        stds = np.std(features, axis=0)

        np.testing.assert_array_almost_equal(means, [0, 0, 0, 0], decimal=10)
        np.testing.assert_array_almost_equal(stds, [1, 1, 1, 1], decimal=10)

        # Check normalization flag
        assert data['normalized'] == True

    def test_split_data(self):
        """Test data splitting."""
        # Create sample data
        X = np.random.rand(100, 4)
        y = np.random.randint(0, 3, 100)

        # Split data
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y, test_size=0.2)

        # Check split sizes
        assert X_train.shape[0] == 80
        assert X_test.shape[0] == 20
        assert y_train.shape[0] == 80
        assert y_test.shape[0] == 20

        # Check feature dimensions are preserved
        assert X_train.shape[1] == X.shape[1]
        assert X_test.shape[1] == X.shape[1]

    def test_get_data_summary(self):
        """Test data summary generation."""
        # Create sample data
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1, 0])

        summary = self.loader.get_data_summary(X, y)

        # Check summary structure
        assert 'n_samples' in summary
        assert 'n_features' in summary
        assert 'n_classes' in summary
        assert 'class_distribution' in summary
        assert 'feature_stats' in summary

        # Check values
        assert summary['n_samples'] == 3
        assert summary['n_features'] == 2
        assert summary['n_classes'] == 2
        assert summary['class_distribution'] == {0: 2, 1: 1}

        # Check feature stats
        expected_means = [3.0, 4.0]  # Mean of [1,3,5] and [2,4,6]
        assert summary['feature_stats']['mean'] == expected_means


class TestPrepareDataPipeline:
    """Test cases for the complete data pipeline."""

    def test_prepare_data_pipeline(self):
        """Test complete data preparation pipeline."""
        result = prepare_data_pipeline()

        # Check all required keys are present
        required_keys = [
            'X_train', 'X_test', 'y_train', 'y_test',
            'feature_names', 'target_names',
            'train_summary', 'test_summary', 'normalized'
        ]

        for key in required_keys:
            assert key in result

        # Check data dimensions
        assert result['X_train'].shape[0] == 120  # 80% of 150
        assert result['X_test'].shape[0] == 30    # 20% of 150
        assert result['X_train'].shape[1] == 4    # 4 features
        assert result['X_test'].shape[1] == 4

        # Check that summaries are dictionaries
        assert isinstance(result['train_summary'], dict)
        assert isinstance(result['test_summary'], dict)

        # Check normalization flag
        assert result['normalized'] == False

    def test_prepare_data_pipeline_normalized(self):
        """Test pipeline with normalization."""
        result = prepare_data_pipeline(normalize=True)

        # Check normalization flag
        assert result['normalized'] == True

        # Check that features are normalized
        X_combined = np.vstack([result['X_train'], result['X_test']])
        means = np.mean(X_combined, axis=0)
        stds = np.std(X_combined, axis=0)

        # Should be close to 0 mean and 1 std (within tolerance due to train/test split)
        assert all(abs(mean) < 0.5 for mean in means)
        assert all(0.5 < std < 1.5 for std in stds)

    def test_prepare_data_pipeline_custom_params(self):
        """Test pipeline with custom parameters."""
        result = prepare_data_pipeline(test_size=0.3, random_state=123)

        # Check split sizes with custom test_size
        assert result['X_train'].shape[0] == 105  # 70% of 150
        assert result['X_test'].shape[0] == 45    # 30% of 150