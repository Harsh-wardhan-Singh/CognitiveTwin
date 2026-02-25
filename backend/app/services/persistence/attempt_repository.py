from sqlalchemy.orm import Session
from app.models.attempt import Attempt


class AttemptRepository:

    @staticmethod
    def save_attempt(
        db: Session,
        user_id: int,
        question_id: int,
        is_correct: bool,
        confidence: int
    ) -> Attempt:
        """
        Persist a single student attempt.
        Does NOT commit. Caller must commit.
        """

        attempt = Attempt(
            user_id=user_id,
            question_id=question_id,
            is_correct=is_correct,
            confidence=confidence
        )

        db.add(attempt)
        return attempt