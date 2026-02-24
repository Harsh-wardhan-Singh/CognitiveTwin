import json

def validate_questions(raw_output: str):
    try:
        data = json.loads(raw_output)

        if "questions" not in data:
            raise ValueError("Missing 'questions' key")

        questions = data["questions"]

        for q in questions:
            required_keys = [
                "question_text",
                "options",
                "base_explanation",
                "concept_tags"
            ]

            for key in required_keys:
                if key not in q:
                    raise ValueError(f"Missing key: {key}")

            if len(q["options"]) < 4:
                raise ValueError("Less than 4 options")

            correct_count = sum(
                1 for o in q["options"] if o["is_correct"]
            )

            if correct_count < 1:
                raise ValueError("No correct answer")

        return questions

    except Exception as e:
        raise ValueError(f"Schema validation failed: {e}")