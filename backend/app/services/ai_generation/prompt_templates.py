def build_question_prompt(topic, difficulty, num_questions):

    return f"""You are a probability exam question generator.

Generate exactly {num_questions} MCQs.
Topic: {topic}
Difficulty: {difficulty}
Audience: High school to early college.

OUTPUT RULES - FOLLOW STRICTLY:
- Output MUST be ONLY valid JSON, nothing else
- NO markdown, NO explanations outside JSON, NO commentary
- Start with {{ and end with }}
- Ensure all quotes are properly escaped
- Ensure all newlines in strings are escaped as \\n
- No trailing commas

JSON FORMAT (strict):
{{
  "questions": [
    {{
      "question_id": "Q1",
      "topic": "{topic}",
      "difficulty": "easy|medium|hard",
      "question_type": "single|multiple",
      "multiple_selectable": true|false,
      "concept_tags": ["tag1", "tag2"],
      "question_text": "text without newlines",
      "options": [
        {{
          "id": "A",
          "text": "option text",
          "is_correct": true|false
        }}
      ],
      "base_explanation": "short explanation"
    }}
  ]
}}

Requirements:
- 4-6 options per question
- At least one correct option
- Mix single and multiple answer questions
- question_text must be under 30 words
- Escape all special characters properly
- Format each string cleanly without rawNewlines

Output ONLY the JSON object, nothing else."""