from app.models.mastery import Mastery
from app.models.mastery_history import MasteryHistory


class MasteryRepository:

    @staticmethod
    def upsert_mastery(
        db,
        user_id,
        concept,
        mastery_value,
        confidence
    ):

        existing = (
            db.query(Mastery)
            .filter(
                Mastery.user_id == user_id,
                Mastery.concept == concept
            )
            .first()
        )

        if existing:
            existing.mastery_value = mastery_value
            existing.confidence = confidence
        else:
            new_mastery = Mastery(
                user_id=user_id,
                concept=concept,
                mastery_value=mastery_value,
                confidence=confidence
            )
            db.add(new_mastery)

        # 🔥 Always insert history snapshot
        history_entry = MasteryHistory(
            user_id=user_id,
            concept=concept,
            mastery_value=mastery_value,
            confidence=confidence
        )

        db.add(history_entry)