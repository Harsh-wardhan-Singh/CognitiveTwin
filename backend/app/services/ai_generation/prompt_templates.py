def build_question_prompt(topic, difficulty, num_questions):

    return f"""
Generate {num_questions} unique probability MCQs.

Topic: {topic}
Difficulty: {difficulty}
Audience: High school to early college

Return JSON in this EXACT format:

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
          "is_correct": true|false
        }}
      ],
      "base_explanation": "Short conceptual explanation (2-4 lines)"
    }}
  ]
}}

Rules:
- 4–6 options per question
- At least one correct option
- Mix single and multiple answer questions
- Avoid repeated numbers
- Keep questions concise
"""