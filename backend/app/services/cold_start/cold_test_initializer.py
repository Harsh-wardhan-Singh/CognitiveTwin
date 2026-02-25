import random


class ColdTestInitializer:

    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor

    def initialize_student(
        self,
        student_state,
        cold_test_results,
        graph
    ):

        # Initialize mastery from cold test accuracy
        for concept, accuracy in cold_test_results.items():
            student_state.mastery_dict[concept] = accuracy
            student_state.attempt_history[concept] = []
            student_state.confidence_metrics[concept] = 0.5

        # Generate initial feature vector
        feature_vector = self.feature_extractor.extract(
            mastery_dict=student_state.mastery_dict,
            attempt_history=student_state.attempt_history,
            confidence_metrics=student_state.confidence_metrics,
            decay_deltas={},
            total_attempts=0
        )

        student_state.global_feature_vector = feature_vector

        return student_state