import random
from typing import List, Dict


class QuizSelector:
    """
    Responsible for selecting questions:
    - 40% common (class-level fairness)
    - 60% personalized (weakest concepts)
    """

    def __init__(self, question_bank: List[Dict]):
        self.question_bank = question_bank

    def select_questions(
        self,
        student_state,
        topic: str,
        total_questions: int
    ) -> List[Dict]:

        topic_questions = [
            q for q in self.question_bank
            if q["topic"] == topic
        ]

        if not topic_questions:
            raise ValueError(f"No questions available for topic: {topic}")

        common_count = int(total_questions * 0.4)
        adaptive_count = total_questions - common_count

        # ------------- COMMON QUESTIONS -------------
        common_questions = random.sample(
            topic_questions,
            min(common_count, len(topic_questions))
        )

        # ------------- ADAPTIVE QUESTIONS -------------
        weakest_concepts = sorted(
            student_state.mastery_dict.items(),
            key=lambda x: x[1]
        )

        adaptive_pool = []
        for concept, _ in weakest_concepts:
            concept_questions = [
                q for q in topic_questions
                if concept in q["concept_tags"]
            ]
            adaptive_pool.extend(concept_questions)

        adaptive_pool = list({q["id"]: q for q in adaptive_pool}.values())

        adaptive_questions = random.sample(
            adaptive_pool,
            min(adaptive_count, len(adaptive_pool))
        )

        selected = common_questions + adaptive_questions
        random.shuffle(selected)

        return selected