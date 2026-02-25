from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.mastery import Mastery
from app.models.attempt import Attempt
from app.models.mastery_history import MasteryHistory


class InsightGenerator:

    # ---------------------------------------------------------
    # Weak Topics (Current Mastery Snapshot)
    # ---------------------------------------------------------
    @staticmethod
    def weak_topics(db: Session, user_id: int, threshold: float = 0.4):
        rows = (
            db.query(Mastery)
            .filter(Mastery.user_id == user_id)
            .all()
        )

        return [
            row.concept
            for row in rows
            if row.mastery_value <= threshold
        ]


    # ---------------------------------------------------------
    # Calibration Gap (Confidence vs Accuracy)
    # ---------------------------------------------------------
    @staticmethod
    def calibration_gap(db: Session, user_id: int):

        attempts = (
            db.query(Attempt)
            .filter(Attempt.user_id == user_id)
            .all()
        )

        if not attempts:
            return 0.0

        avg_confidence = sum(a.confidence for a in attempts) / len(attempts)
        accuracy = sum(1 if a.is_correct else 0 for a in attempts) / len(attempts)

        return round(avg_confidence - accuracy, 4)


    # ---------------------------------------------------------
    # Volatility per Concept (True Temporal Instability)
    # ---------------------------------------------------------
    @staticmethod
    def volatility_score(db: Session, user_id: int, concept: str, window: int = 10):

        history = (
            db.query(MasteryHistory)
            .filter(
                MasteryHistory.user_id == user_id,
                MasteryHistory.concept == concept
            )
            .order_by(MasteryHistory.timestamp.desc())
            .limit(window)
            .all()
        )

        if len(history) < 2:
            return 0.0

        values = [h.mastery_value for h in history]

        diffs = [
            abs(values[i] - values[i + 1])
            for i in range(len(values) - 1)
        ]

        return round(sum(diffs) / len(diffs), 4)


    # ---------------------------------------------------------
    # Learning Trend per Concept (Slope Approximation)
    # ---------------------------------------------------------
    @staticmethod
    def learning_trend(db: Session, user_id: int, concept: str, window: int = 10):

        history = (
            db.query(MasteryHistory)
            .filter(
                MasteryHistory.user_id == user_id,
                MasteryHistory.concept == concept
            )
            .order_by(MasteryHistory.timestamp.asc())
            .limit(window)
            .all()
        )

        if len(history) < 2:
            return 0.0

        start = history[0].mastery_value
        end = history[-1].mastery_value

        return round(end - start, 4)


    # ---------------------------------------------------------
    # Full Student Insight Package
    # ---------------------------------------------------------
    @staticmethod
    def generate_student_insights(db: Session, user_id: int):

        # Get all concepts student currently has
        mastery_rows = (
            db.query(Mastery)
            .filter(Mastery.user_id == user_id)
            .all()
        )

        concepts = [row.concept for row in mastery_rows]

        concept_dynamics = {}

        for concept in concepts:
            concept_dynamics[concept] = {
                "volatility": InsightGenerator.volatility_score(
                    db, user_id, concept
                ),
                "learning_trend": InsightGenerator.learning_trend(
                    db, user_id, concept
                )
            }

        return {
            "weak_topics": InsightGenerator.weak_topics(db, user_id),
            "calibration_gap": InsightGenerator.calibration_gap(db, user_id),
            "concept_dynamics": concept_dynamics
        }