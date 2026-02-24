import numpy as np


class ConfidenceModel:
    """
    Computes statistical certainty of mastery.
    """

    def compute(self, attempts: list):
        """
        attempts: list of 1 (correct) / 0 (incorrect)

        returns confidence score (0–1)
        """

        if len(attempts) == 0:
            return 0.0

        mean = np.mean(attempts)
        variance = np.var(attempts)

        stability = 1 - variance
        volume_factor = min(1.0, len(attempts) / 10)

        confidence_score = stability * volume_factor

        return confidence_score