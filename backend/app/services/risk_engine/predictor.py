import os
import joblib
import numpy as np
from typing import Dict, Any
from app.services.risk_engine.feature_schema import FEATURE_ORDER


class RiskPredictor:

    def __init__(self, model_path: str = None):
        """
        If model_path is not provided,
        load from risk_engine/models/risk_model.joblib
        """

        if model_path is None:
            base_dir = os.path.dirname(__file__)
            model_path = os.path.join(
                base_dir,
                "models",
                "risk_model.joblib"
            )

        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load risk model from {model_path}: {e}"
            )

    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:

        missing = [f for f in FEATURE_ORDER if f not in features]
        if missing:
            raise ValueError(f"Missing required features: {missing}")

        feature_vector = np.array(
            [[features[name] for name in FEATURE_ORDER]],
            dtype=np.float32
        )

        probability = float(
            self.model.predict_proba(feature_vector)[0][1]
        )

        risk_level = self._risk_level(probability)
        confidence_score = abs(probability - 0.5) * 2

        return {
        "risk_probability": probability,
        "risk_level": risk_level,
        "confidence_score": confidence_score,
        "feature_vector": feature_vector.tolist(),
        "features": features,
        }

    @staticmethod
    def _risk_level(probability: float) -> str:
        if probability < 0.3:
            return "low"
        elif probability < 0.7:
            return "medium"
        else:
            return "high"