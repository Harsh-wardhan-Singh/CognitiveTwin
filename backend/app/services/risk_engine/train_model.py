import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

from feature_schema import FEATURE_ORDER


def load_from_csv(path):
    df = pd.read_csv(path)

    X = df[FEATURE_ORDER].values
    y = df["risk_label"].values

    return X, y


def train_model(data_path, save_path):

    print("Loading dataset...")
    X, y = load_from_csv(data_path)

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Building pipeline...")
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            C=1.0,
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        ))
    ])

    print("Training...")
    model.fit(X_train, y_train)

    print("Evaluating...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")

    joblib.dump(model, save_path)
    print(f"Model saved to {save_path}")


if __name__ == "__main__":
    DATA_PATH = r".\backend\app\services\risk_engine\data\risk_training_dataset_500.csv"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MODEL_DIR = os.path.join(BASE_DIR, "models")
    os.makedirs(MODEL_DIR, exist_ok=True)

    SAVE_PATH = os.path.join(MODEL_DIR, "risk_model.joblib")   

    train_model(DATA_PATH, SAVE_PATH)