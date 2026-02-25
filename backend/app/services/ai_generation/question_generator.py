import time
import json
from .llm_client import LLMClient, LLMTransportError
from .prompt_templates import build_question_prompt
from .schema_validator import validate_questions


MAX_RETRIES = 3
RETRY_DELAY = 1.5


class QuestionGenerationError(Exception):
    pass


class QuestionGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def _safe_generate(self, system_prompt, prompt):

        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                raw = self.llm.generate_json(system_prompt, prompt)

                # Ensure JSON parsing is explicit
                parsed = json.loads(raw)

                questions = validate_questions(parsed)
                return questions

            except LLMTransportError:
                # Transport errors should immediately bubble up
                raise

            except (json.JSONDecodeError, ValueError) as e:
                # Schema or parsing issue — retry
                last_error = e

                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    break

        raise QuestionGenerationError(
            f"Question generation failed after {MAX_RETRIES} attempts: {last_error}"
        )

    def generate_quiz(self, weak_topics, total_questions, difficulty):

        baseline_count = round(total_questions * 0.4)
        adaptive_count = total_questions - baseline_count

        questions = []

        system_prompt = "You are an expert probability educator."

        # BASELINE QUESTIONS
        baseline_prompt = build_question_prompt(
            topic="General Probability",
            difficulty=difficulty,
            num_questions=baseline_count
        )

        baseline_questions = self._safe_generate(
            system_prompt,
            baseline_prompt
        )

        questions.extend(baseline_questions)

        # ADAPTIVE QUESTIONS
        if weak_topics and adaptive_count > 0:

            per_topic = max(1, adaptive_count // len(weak_topics))

            for topic in weak_topics:

                prompt = build_question_prompt(
                    topic=topic,
                    difficulty=difficulty,
                    num_questions=per_topic
                )

                topic_questions = self._safe_generate(
                    system_prompt,
                    prompt
                )

                questions.extend(topic_questions)

        return questions