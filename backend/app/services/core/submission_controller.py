from app.services.core.event_bus import EventBus


class SubmissionController:

    def __init__(
        self,
        cognitive_pipeline,
        training_store
    ):
        self.pipeline = cognitive_pipeline
        self.training_store = training_store

    def submit_answer(
        self,
        student_state,
        class_id,
        concept,
        correct,
        response_time,
        confidence,
        total_attempts,
        class_states
    ):

        result = self.pipeline.process_submission(
            student_state=student_state,
            concept=concept,
            correct=correct,
            response_time=response_time,
            student_confidence=confidence,
            total_attempts=total_attempts,
            class_states=class_states
        )

        # Store training data
        self.training_store.append(
            result["risk"]["feature_vector"],
            result["risk"]["risk_label"]
        )

        # Push update to teacher
        EventBus.push_teacher_update(
            class_id=class_id,
            payload={
                "student_id": student_state.student_id,
                "mastery_delta": result["mastery_delta"],
                "risk": result["risk"]
            }
        )

        return {
            "mastery": result["updated_mastery"],
            "delta": result["mastery_delta"],
            "risk": result["risk"]
        }