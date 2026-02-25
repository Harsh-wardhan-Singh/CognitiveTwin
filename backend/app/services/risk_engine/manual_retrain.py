import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression


class ManualRetrainer:

    def __init__(self, training_data_store: list, model_output_path: str):
        self.training_data_store = training_data_store
        self.model_output_path = model_output_path

    def retrain(self):

        if len(self.training_data_store) < 50:
            raise ValueError("Not enough data to retrain.")

        X = np.array([item["features"] for item in self.training_data_store])
        y = np.array([item["label"] for item in self.training_data_store])

        model = LogisticRegression(
            class_weight="balanced",
            max_iter=1000
        )

        model.fit(X, y)

        joblib.dump(model, self.model_output_path)

        return {
            "status": "Model retrained successfully",
            "samples_used": len(X)
        }