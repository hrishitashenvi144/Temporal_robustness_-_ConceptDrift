"""
Feature-Distribution Drift Detection Module
============================================

Methodological Note:
This detector measures feature-distribution shift P(X); it does not establish
concept drift P(Y|X).

Reference distribution: Training period features (e.g., period_old).
Test distribution: Incoming future cohort features (e.g., period_medium).

Threshold Note:
The drift threshold (default 0.10 for Phase 2 controlled experiments) is a configured
experimental parameter and is not claimed to be statistically optimal. Threshold
sensitivity and calibration will be evaluated in subsequent research phases.
"""

import logging
from typing import Any, Dict, List

import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance

logger = logging.getLogger(__name__)


class DriftDetector:
    """
    Detects feature-distribution shift P(X) using statistical distance metrics.
    
    Supported methods:
    - 'combined': Average of normalized mean shift and normalized Wasserstein distance.
    - 'wasserstein': Normalized Wasserstein distance across feature dimensions.
    - 'ks': Kolmogorov-Smirnov 2-sample test statistic across feature dimensions.
    """

    def __init__(
        self,
        reference_data: np.ndarray,
        threshold: float = 0.10,
        method: str = "combined"
    ):
        """
        Args:
            reference_data: Feature matrix of the reference cohort (period_old).
            threshold: Configured drift detection threshold (default: 0.10).
            method: Distance metric to use ('combined', 'wasserstein', or 'ks').
        """
        self.reference_data = np.asarray(reference_data, dtype=float)
        if self.reference_data.ndim != 2:
            raise ValueError(f"reference_data must be a 2D array, got shape {self.reference_data.shape}")

        self.reference_mean = self.reference_data.mean(axis=0)
        self.reference_std = self.reference_data.std(axis=0)
        self.threshold = float(threshold)
        self.method = str(method).lower()
        self.drift_history: List[Dict[str, Any]] = []

        logger.info(
            f"Drift detector initialized with {len(self.reference_data)} reference samples, "
            f"method='{self.method}', threshold={self.threshold:.3f}"
        )

    def _ks_test(self, new_data: np.ndarray) -> float:
        """Kolmogorov-Smirnov test for feature-distribution shift."""
        ks_stats = []
        n_features = new_data.shape[1]
        for i in range(n_features):
            statistic, _ = ks_2samp(self.reference_data[:, i], new_data[:, i])
            ks_stats.append(statistic)
        return float(np.mean(ks_stats))

    def _wasserstein_distance(self, new_data: np.ndarray) -> float:
        """Normalized Wasserstein distance across feature dimensions."""
        distances = []
        n_features = new_data.shape[1]
        for i in range(n_features):
            dist = wasserstein_distance(self.reference_data[:, i], new_data[:, i])
            distances.append(dist)

        normalized = [
            dist / (self.reference_std[i] + 1e-6)
            for i, dist in enumerate(distances)
        ]
        return float(np.mean(normalized))

    def _mean_shift(self, new_data: np.ndarray) -> float:
        """Normalized shift in feature means."""
        mean_shift = np.abs(new_data.mean(axis=0) - self.reference_mean)
        normalized_shift = mean_shift / (self.reference_std + 1e-6)
        return float(np.mean(normalized_shift))

    def detect_drift(self, new_data: np.ndarray) -> Dict[str, Any]:
        """
        Detect whether incoming feature data exhibits distribution shift P(X)
        exceeding the configured threshold.

        Returns:
            Dict containing:
            - 'drift_detected': bool
            - 'drift_score': float
            - 'threshold': float
            - 'recommendation': str ('RETRAIN' or 'MONITOR')
        """
        new_data = np.asarray(new_data, dtype=float)
        if new_data.ndim != 2:
            raise ValueError(f"new_data must be a 2D array, got shape {new_data.shape}")

        if new_data.shape[1] != self.reference_data.shape[1]:
            raise ValueError(
                f"Feature dimension mismatch: expected {self.reference_data.shape[1]}, "
                f"got {new_data.shape[1]}"
            )

        if self.method == "ks":
            drift_score = self._ks_test(new_data)
        elif self.method == "wasserstein":
            drift_score = self._wasserstein_distance(new_data)
        elif self.method == "combined":
            score1 = self._mean_shift(new_data)
            score2 = self._wasserstein_distance(new_data)
            drift_score = (score1 + score2) / 2.0
        else:
            raise ValueError(f"Unknown drift detection method: {self.method}")

        drift_detected = bool(drift_score > self.threshold)

        result = {
            "drift_detected": drift_detected,
            "drift_score": float(drift_score),
            "threshold": float(self.threshold),
            "recommendation": "RETRAIN" if drift_detected else "MONITOR"
        }

        self.drift_history.append(result)
        return result