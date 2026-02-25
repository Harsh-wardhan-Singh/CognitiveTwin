from datetime import datetime


class StudentState:

    def __init__(self, student_id: str):
        self.student_id = student_id

        self.mastery_dict = {}
        self.attempt_history = {}
        self.confidence_metrics = {}
        self.last_attempt_time = {}

        self.risk_profile = None
        self.decay_deltas_cache = {}

        self.mastery_history = []

        # 17-feature baseline (cold test)
        self.global_feature_vector = [0.0] * 17

    def compute_decay_deltas(self):
        return self.decay_deltas_cache

    def snapshot_mastery(self):
        return self.mastery_dict.copy()

    def log_mastery_change(self, concept, old, new):
        self.mastery_history.append({
            "concept": concept,
            "old": old,
            "new": new,
            "timestamp": datetime.now()
        })