from .llm_client import LLMClient


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

        return self.llm.generate_json(system_prompt, user_prompt)