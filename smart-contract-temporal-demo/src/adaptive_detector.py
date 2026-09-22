"""
Adaptive Vulnerability Detector
Automatically retrains when drift is detected
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
from drift_detector import DriftDetector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptiveDetector:
    """
    Detector that adapts by retraining when drift is detected
    """
    
    def __init__(self, model=None, drift_threshold=0.25):
        if model is None:
            self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        else:
            self.model = model
        self.drift_threshold = drift_threshold
        self.drift_detector = None
        self.retrain_history = []
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def fit(self, X_train, y_train):
        """Initial training"""
        logger.info(f"Training adaptive detector on {len(X_train)} samples...")
        
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        
        # Initialize drift detector
        self.drift_detector = DriftDetector(X_scaled, threshold=self.drift_threshold)
        
        logger.info(f"Adaptive detector fitted successfully")
        return self
    
    def predict(self, X):
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def predict_proba(self, X):
        """Get prediction probabilities"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
    
    def evaluate_and_adapt(self, X_test, y_test, period_name, X_retrain=None, y_retrain=None):
        """
        Evaluate on new data
        Detect drift
        Retrain if needed
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        X_scaled = self.scaler.transform(X_test)
        
        # Current performance
        y_pred = self.model.predict(X_scaled)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='binary', zero_division=0
        )
        
        # Detect drift
        drift_info = self.drift_detector.detect_drift(X_scaled)
        
        # Decide if we should retrain
        retrained = False
        f1_after = f1
        
        if drift_info['drift_detected']:
            logger.warning(f"\n🔴 DRIFT DETECTED in {period_name}!")
            logger.warning(f"   Drift score: {drift_info['drift_score']:.3f}")
            logger.warning(f"   F1-Score before retrain: {f1:.3f}")
            
            if X_retrain is not None and y_retrain is not None:
                # Retrain on accumulated data
                X_retrain_scaled = self.scaler.fit_transform(X_retrain)
                self.model.fit(X_retrain_scaled, y_retrain)
                
                # Evaluate after retraining
                y_pred_after = self.model.predict(X_scaled)
                _, _, f1_after, _ = precision_recall_fscore_support(
                    y_test, y_pred_after, average='binary', zero_division=0
                )
                
                logger.info(f"   Retrained on {len(X_retrain)} samples")
                logger.info(f"   F1-Score after retrain: {f1_after:.3f}")
                logger.info(f"   Recovery: +{f1_after - f1:.3f}")
                
                retrained = True
                self.retrain_history.append(period_name)
        
        return {
            'Period': period_name,
            'F1_Before': f1,
            'Precision': precision,
            'Recall': recall,
            'F1_After': f1_after,
            'Drift_Detected': drift_info['drift_detected'],
            'Drift_Score': drift_info['drift_score'],
            'Retrained': retrained
        }