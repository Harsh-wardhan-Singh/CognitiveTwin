from dataclasses import dataclass


@dataclass
class BKTParameters:
    p_init: float      # Initial mastery
    p_learn: float     # Learning probability
    p_guess: float     # Guess probability
    p_slip: float      # Slip probability


class MasteryUpdater:
    """
    Advanced Bayesian Knowledge Tracing
    Supports:
    - Concept-specific parameters
    - Self-confidence weighting
    """

    def __init__(self, concept_params: dict):
        """
        concept_params:
        {
            "limits": BKTParameters(...),
            "derivatives": BKTParameters(...),
        }
        """
        self.concept_params = concept_params

    def update(self, concept: str, current_mastery: float,
               correct: bool, self_confidence: int):
        """
        concept          : concept name
        current_mastery  : float (0–1)
        correct          : bool
        self_confidence  : int (1–5 scale)

        returns updated mastery
        """

        params = self.concept_params[concept]

        p_l = current_mastery

        # ---- 1️⃣ Bayesian update ----
        if correct:
            numerator = p_l * (1 - params.p_slip)
            denominator = numerator + (1 - p_l) * params.p_guess
        else:
            numerator = p_l * params.p_slip
            denominator = numerator + (1 - p_l) * (1 - params.p_guess)

        if denominator == 0:
            p_posterior = p_l
        else:
            p_posterior = numerator / denominator

        # ---- 2️⃣ Confidence weighting ----
        confidence_weight = self._confidence_weight(self_confidence, correct)
        p_posterior = p_posterior * confidence_weight + p_l * (1 - confidence_weight)

        # ---- 3️⃣ Learning transition ----
        p_new = p_posterior + (1 - p_posterior) * params.p_learn

        return max(0.0, min(1.0, p_new))

    def _confidence_weight(self, self_confidence: int, correct: bool):
        """
        Adjust how strongly the answer affects mastery.
        High confidence wrong answers penalize more.
        High confidence correct answers reward more.
        """

        scale = self_confidence / 5.0  # normalize 0–1

        if correct:
            return 0.6 + 0.4 * scale
        else:
            return 0.6 + 0.4 * scale