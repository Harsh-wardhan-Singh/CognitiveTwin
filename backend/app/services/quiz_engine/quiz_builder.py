from typing import List, Dict
import random


class QuizBuilder:
    """
    Teacher-controlled quiz generator.
    Inputs:
        - topic
        - number_of_questions
        - difficulty
    """

    def __init__(self, question_bank: List[Dict]):
        self.question_bank = question_bank

    def build_quiz(
        self,
        topic: str,
        number_of_questions: int,
        difficulty: str
    ) -> List[Dict]:

        filtered = [
            q for q in self.question_bank
            if q["topic"] == topic and q["difficulty"] == difficulty
        ]

        if len(filtered) < number_of_questions:
            raise ValueError("Not enough questions available.")

        return random.sample(filtered, number_of_questions)