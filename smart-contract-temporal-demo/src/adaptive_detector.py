"""
Adaptive Vulnerability Detector Module
=======================================

Detects feature-distribution drift P(X) and retrains model on newly available historical data.

Protocol Constraints:
- Scaler is fitted strictly on available training data (never on test data).
- evaluate() and detect_drift() are read-only and perform no hidden mutations.
- retrain() explicitly refits scaler and model on cumulative training data.
- All logging is strictly ASCII-safe for cross-platform compatibility.
"""

import logging
from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler

from drift_detector import DriftDetector

logger = logging.getLogger(__name__)


class AdaptiveDetector:
    """
    Adaptive vulnerability detector for smart contracts.

    Lifecycle:
    1. Initial fit on period_old training data.
    2. Read-only evaluation on incoming test cohorts.
    3. Drift detection on incoming feature vectors X.
    4. Controlled retraining if drift is detected, using strictly cumulative historical data.
    """

    def __init__(
        self,
        model: Optional[RandomForestClassifier] = None,
        drift_threshold: float = 0.10,
        drift_method: str = "combined"
    ):
        if model is None:
            self.model = RandomForestClassifier(
                n_estimators=50,
                random_state=42
            )
        else:
            self.model = model

        self.drift_threshold = float(drift_threshold)
        self.drift_method = str(drift_method)
        self.drift_detector: Optional[DriftDetector] = None
        self.retrain_history: List[str] = []

        self.scaler = StandardScaler()
        self.is_trained: bool = False
        self.training_sample_count: int = 0
        self.last_evaluation_sample_count: int = 0

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "AdaptiveDetector":
        """
        Initial training on the historical reference cohort (period_old).
        Fits scaler strictly on X_train and establishes drift reference.
        """
        X_arr = np.asarray(X_train, dtype=float)
        y_arr = np.asarray(y_train, dtype=int)

        self.training_sample_count = len(X_arr)
        logger.info(f"Training adaptive detector on {self.training_sample_count} samples...")

        # Scaler fitted strictly on training data
        X_scaled = self.scaler.fit_transform(X_arr)

        self.model.fit(X_scaled, y_arr)
        self.is_trained = True

        # Scaled training distribution serves as reference distribution for drift detection
        self.drift_detector = DriftDetector(
            X_scaled,
            threshold=self.drift_threshold,
            method=self.drift_method
        )

        logger.info("Adaptive detector fitted successfully.")
        return self

    def _check_trained(self) -> None:
        if not self.is_trained:
            raise ValueError("AdaptiveDetector must be trained via fit() before prediction or evaluation.")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Generate class predictions using frozen current model and scaler.
        """
        self._check_trained()
        X_arr = np.asarray(X, dtype=float)
        X_scaled = self.scaler.transform(X_arr)
        return self.model.predict(X_scaled)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Generate class probabilities using frozen current model and scaler.
        """
        self._check_trained()
        X_arr = np.asarray(X, dtype=float)
        X_scaled = self.scaler.transform(X_arr)
        return self.model.predict_proba(X_scaled)

    def evaluate(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        period_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate current model on a test cohort without mutating model, scaler, or drift state.
        """
        self._check_trained()

        X_arr = np.asarray(X_test, dtype=float)
        y_arr = np.asarray(y_test, dtype=int)
        self.last_evaluation_sample_count = len(X_arr)

        X_scaled = self.scaler.transform(X_arr)
        y_pred = self.model.predict(X_scaled)

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_arr,
            y_pred,
            average="binary",
            zero_division=0
        )

        return {
            "Period": period_name,
            "Precision": float(precision),
            "Recall": float(recall),
            "F1": float(f1),
            "Evaluation_Samples": len(X_arr)
        }

    def detect_drift(
        self,
        X_test: np.ndarray,
        period_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect feature-distribution shift on X_test without modifying the model.
        """
        self._check_trained()

        X_arr = np.asarray(X_test, dtype=float)
        X_scaled = self.scaler.transform(X_arr)

        drift_info = self.drift_detector.detect_drift(X_scaled)

        period_label = period_name or "current cohort"
        if drift_info["drift_detected"]:
            logger.warning(
                f"[DRIFT DETECTED] in {period_label}! Score: {drift_info['drift_score']:.3f} "
                f"(Threshold: {drift_info['threshold']:.3f})"
            )
        else:
            logger.info(
                f"[NO DRIFT] in {period_label}. Score: {drift_info['drift_score']:.3f} "
                f"(Threshold: {drift_info['threshold']:.3f})"
            )

        return drift_info

    def retrain(
        self,
        X_retrain: np.ndarray,
        y_retrain: np.ndarray,
        period_name: Optional[str] = None
    ) -> "AdaptiveDetector":
        """
        Retrain model and refit preprocessing on cumulative data available up to this point.
        Evaluation on new data must occur separately after this step.
        """
        self._check_trained()

        X_arr = np.asarray(X_retrain, dtype=float)
        y_arr = np.asarray(y_retrain, dtype=int)

        self.training_sample_count = len(X_arr)
        logger.info(f"Retraining adaptive detector on {self.training_sample_count} cumulative samples...")

        # Refit scaler and model on cumulative dataset
        X_retrain_scaled = self.scaler.fit_transform(X_arr)
        self.model.fit(X_retrain_scaled, y_arr)

        if period_name:
            self.retrain_history.append(period_name)

        logger.info(
            f"Adaptive detector retrained successfully"
            f"{f' at {period_name}' if period_name else ''}."
        )

        return self

    def evaluate_and_detect(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        period_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method to evaluate current performance and detect drift on incoming cohort.
        Does NOT trigger retraining.
        """
        evaluation = self.evaluate(X_test, y_test, period_name=period_name)
        drift_info = self.detect_drift(X_test, period_name=period_name)

        return {
            **evaluation,
            "Drift_Detected": drift_info["drift_detected"],
            "Drift_Score": drift_info["drift_score"],
            "Drift_Threshold": drift_info["threshold"]
        }