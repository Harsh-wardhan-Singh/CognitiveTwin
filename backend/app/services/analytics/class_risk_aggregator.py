from sqlalchemy.orm import Session
from app.models.mastery import Mastery


class ClassRiskAggregator:

    @staticmethod
    def aggregate_from_mastery(db: Session, threshold: float = 0.4):
        """
        Computes class-level risk using low mastery threshold.
        """

        rows = db.query(Mastery).all()

        student_scores = {}

        for row in rows:
            if row.user_id not in student_scores:
                student_scores[row.user_id] = []

            student_scores[row.user_id].append(row.mastery_value)

        student_risk = {}

        for student, values in student_scores.items():
            avg_mastery = sum(values) / len(values)
            risk = 1 - avg_mastery
            student_risk[student] = risk

        high_risk = [
            student for student, risk in student_risk.items()
            if risk >= (1 - threshold)
        ]

        class_average_risk = (
            sum(student_risk.values()) / len(student_risk)
            if student_risk else 0
        )

        return {
            "class_average_risk": class_average_risk,
            "high_risk_students": high_risk,
            "student_risk_map": student_risk
        }