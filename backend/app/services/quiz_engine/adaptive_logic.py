class AdaptiveLogic:
    """
    Controls dynamic difficulty adjustments
    based on student streak and confidence.
    """

    def __init__(self):
        self.streak_threshold = 3

    def adjust_difficulty(
        self,
        current_difficulty: str,
        recent_attempts: list
    ) -> str:

        if len(recent_attempts) < self.streak_threshold:
            return current_difficulty

        last_three = recent_attempts[-3:]

        if all(last_three):
            return self._increase(current_difficulty)

        if not any(last_three):
            return self._decrease(current_difficulty)

        return current_difficulty

    def _increase(self, difficulty):
        levels = ["easy", "medium", "hard"]
        idx = levels.index(difficulty)
        return levels[min(idx + 1, 2)]

    def _decrease(self, difficulty):
        levels = ["easy", "medium", "hard"]
        idx = levels.index(difficulty)
        return levels[max(idx - 1, 0)]