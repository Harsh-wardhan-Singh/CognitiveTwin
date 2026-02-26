import math
from datetime import datetime


class RetentionDecay:
    """
    Applies exponential forgetting curve.
    """

    def __init__(self, base_decay_rate=0.01):
        self.base_decay_rate = base_decay_rate

    def apply_decay(self, mastery: float, last_attempt_time: datetime,
              current_time: datetime):
        """
        mastery            : current mastery
        last_attempt_time  : datetime
        current_time       : datetime

        returns decayed mastery
        """

        time_gap = (current_time - last_attempt_time).total_seconds() / 86400  # days

        decay = math.exp(-self.base_decay_rate * time_gap)

        return mastery * decay