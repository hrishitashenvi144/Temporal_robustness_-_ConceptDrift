"""
Drift Detection Module
Detects concept drift in smart contract feature distributions
"""

import numpy as np
from scipy.stats import wasserstein_distance
from scipy.stats import ks_2samp
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """
    Detects concept drift using multiple statistical methods
    """
    
    def __init__(self, reference_data, threshold=0.25, method='combined'):
        """
        Args:
            reference_data: Training period features (numpy array)
            threshold: Drift detection threshold (0-1)
            method: 'ks', 'wasserstein', or 'combined'
        """
        self.reference_data = reference_data
        self.reference_mean = reference_data.mean(axis=0)
        self.reference_std = reference_data.std(axis=0)
        self.threshold = threshold
        self.method = method
        self.drift_history = []
        
        logger.info(f"Drift detector initialized with {len(reference_data)} reference samples")
    
    def _ks_test(self, new_data):
        """Kolmogorov-Smirnov test for distribution shift"""
        ks_stats = []
        
        for i in range(new_data.shape[1]):
            statistic, p_value = ks_2samp(self.reference_data[:, i], new_data[:, i])
            ks_stats.append(statistic)
        
        return np.mean(ks_stats)
    
    def _wasserstein_distance(self, new_data):
        """Wasserstein distance between distributions"""
        distances = []
        
        for i in range(new_data.shape[1]):
            dist = wasserstein_distance(self.reference_data[:, i], new_data[:, i])
            distances.append(dist)
        
        # Normalize by std
        normalized = [d / (self.reference_std[i] + 1e-6) for i, d in enumerate(distances)]
        return np.mean(normalized)
    
    def _mean_shift(self, new_data):
        """Detect shift in mean"""
        mean_shift = np.abs(new_data.mean(axis=0) - self.reference_mean)
        normalized_shift = mean_shift / (self.reference_std + 1e-6)
        return np.mean(normalized_shift)
    
    def detect_drift(self, new_data):
        """
        Detect if new data has significant drift
        
        Returns:
            dict with drift_detected, drift_score, recommendation
        """
        new_data = np.array(new_data)
        
        if self.method == 'ks':
            drift_score = self._ks_test(new_data)
        elif self.method == 'wasserstein':
            drift_score = self._wasserstein_distance(new_data)
        else:  # combined
            score1 = self._mean_shift(new_data)
            score2 = self._wasserstein_distance(new_data)
            drift_score = (score1 + score2) / 2
        
        drift_detected = drift_score > self.threshold
        
        result = {
            'drift_detected': drift_detected,
            'drift_score': drift_score,
            'threshold': self.threshold,
            'recommendation': 'RETRAIN' if drift_detected else 'MONITOR'
        }
        
        self.drift_history.append(result)
        
        return result