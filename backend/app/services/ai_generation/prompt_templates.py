def build_question_prompt(topic, difficulty, num_questions):

    return f"""
You are a probability exam question generator.

Generate exactly {num_questions} MCQs.
Topic: {topic}
Difficulty: {difficulty}
Audience: High school to early college.

IMPORTANT:
- Output MUST be valid JSON.
- Do NOT include explanations outside JSON.
- Do NOT include markdown.
- Do NOT include commentary.
- Start with {{ and end with }}.

JSON FORMAT:

{{
  "questions": [
    {{
      "question_id": "string",
      "topic": "string",
      "difficulty": "easy|medium|hard",
      "question_type": "single|multiple",
      "multiple_selectable": true|false,
      "concept_tags": ["tag1", "tag2"],
      "question_text": "string under 30 words",
      "options": [
        {{
          "id": "A",
          "text": "string",
          "is_correct": true
        }}
      ],
      "base_explanation": "2-4 line explanation"
    }}
  ]
}}

Rules:
- 4–6 options per question
- At least one correct option
- Mix single and multiple answer questions
- Avoid repeated numbers
- Keep questions concise

Return ONLY JSON.
"""