import json
import os
from datetime import datetime


class TrainingDataStore:

    def __init__(self, path="training_data.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def append(self, features, label):
        with open(self.path, "r") as f:
            data = json.load(f)

        data.append({
            "features": features,
            "label": label,
            "timestamp": datetime.now().isoformat()
        })

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load_all(self):
        with open(self.path, "r") as f:
            return json.load(f)