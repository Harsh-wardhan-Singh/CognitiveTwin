from .llm_client import LLMClient
from .prompt_templates import build_question_prompt
from .schema_validator import validate_questions


class QuestionGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate_quiz(self, weak_topics, total_questions, difficulty):

        baseline_count = round(total_questions * 0.4)
        adaptive_count = total_questions - baseline_count

        questions = []

        system_prompt = "You are an expert probability educator."

        # Baseline
        baseline_prompt = build_question_prompt(
            topic="General Probability",
            difficulty=difficulty,
            num_questions=baseline_count
        )

        baseline_raw = self.llm.generate_json(system_prompt, baseline_prompt)
        baseline_questions = validate_questions(baseline_raw)
        questions.extend(baseline_questions)

        # Adaptive
        per_topic = max(1, adaptive_count // len(weak_topics))

        for topic in weak_topics:
            prompt = build_question_prompt(
                topic=topic,
                difficulty=difficulty,
                num_questions=per_topic
            )

            raw = self.llm.generate_json(system_prompt, prompt)
            topic_questions = validate_questions(raw)
            questions.extend(topic_questions)

        return questions