import joblib
import numpy as np


class RiskModel:
    def __init__(self, model_path: str = None):
        self.model = None
        self.is_trained = False

        if model_path:
            self.load(model_path)

    # --------------------------------------------------
    # Training
    # --------------------------------------------------

    def train(self, X: np.ndarray, y: np.ndarray):
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression

        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(
                C=1.0,
                class_weight="balanced",
                max_iter=1000,
                random_state=42
            ))
        ])

        self.model.fit(X, y)
        self.is_trained = True

    # --------------------------------------------------

    def predict_proba(self, X: np.ndarray):
        if not self.is_trained:
            raise ValueError("Model not trained or loaded.")

        return self.model.predict_proba(X)[:, 1]

    def predict(self, X: np.ndarray, threshold: float = 0.5):
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)

    # --------------------------------------------------

    def save(self, path: str):
        joblib.dump(self.model, path)

    def load(self, path: str):
        self.model = joblib.load(path)
        self.is_trained = True