import time
import json
from .llm_client import LLMClient, LLMTransportError
from .schema_validator import validate_explanation


MAX_RETRIES = 3
RETRY_DELAY = 1.5


class ExplanationGenerationError(Exception):
    pass


class ExplanationGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate_adaptive_explanation(
        self,
        question,
        student_answer,
        mastery_score,
        weak_topics,
        confidence_score
    ):

        system_prompt = "You are an adaptive AI probability tutor."

        user_prompt = f"""
Question:
{question['question_text']}

Options:
{question['options']}

Correct Explanation:
{question['base_explanation']}

Student selected:
{student_answer}

Student mastery score: {mastery_score}
Confidence score: {confidence_score}
Weak topics: {weak_topics}

Generate a personalized explanation:
- If mastery < 0.5 → explain step-by-step from fundamentals
- If mastery between 0.5–0.75 → moderate depth
- If mastery high → concise conceptual explanation
- If answer incorrect → explain why their choice is wrong
- Use clear math reasoning
- Do not repeat the question text
Return JSON:
{{
  "adaptive_explanation": "string"
}}
"""

        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                raw = self.llm.generate_json(system_prompt, user_prompt)

                parsed = json.loads(raw)
                return validate_explanation(parsed)

            except LLMTransportError:
                raise

            except (json.JSONDecodeError, ValueError) as e:
                last_error = e

                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    break

        raise ExplanationGenerationError(
            f"Explanation generation failed after {MAX_RETRIES} attempts: {last_error}"
        )