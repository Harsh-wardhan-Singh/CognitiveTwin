import json
from .exceptions import SchemaValidationError

def validate_questions(raw_output: str):
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise SchemaValidationError(f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise SchemaValidationError("Root must be object")

    if "questions" not in data:
        raise SchemaValidationError("Missing 'questions' key")

    if not isinstance(data["questions"], list):
        raise SchemaValidationError("'questions' must be list")

    validated_questions = []

    for q in data["questions"]:

        required_keys = [
            "question_id",
            "topic",
            "difficulty",
            "question_type",
            "multiple_selectable",
            "concept_tags",
            "question_text",
            "options",
            "base_explanation"
        ]

        for key in required_keys:
            if key not in q:
                raise SchemaValidationError(f"Missing key: {key}")

        if not isinstance(q["question_text"], str):
            raise SchemaValidationError("question_text must be string")

        if q["difficulty"] not in ["easy", "medium", "hard"]:
            raise SchemaValidationError("Invalid difficulty")

        if not isinstance(q["multiple_selectable"], bool):
            raise SchemaValidationError("multiple_selectable must be bool")

        if not isinstance(q["concept_tags"], list):
            raise SchemaValidationError("concept_tags must be list")

        if not isinstance(q["options"], list):
            raise SchemaValidationError("options must be list")

        if len(q["options"]) < 4:
            raise SchemaValidationError("Less than 4 options")

        correct_count = 0

        for option in q["options"]:
            if not isinstance(option["id"], str):
                raise SchemaValidationError("Option id must be string")
            if not isinstance(option["text"], str):
                raise SchemaValidationError("Option text must be string")
            if not isinstance(option["is_correct"], bool):
                raise SchemaValidationError("is_correct must be bool")
            if option["is_correct"]:
                correct_count += 1

        if correct_count < 1:
            raise SchemaValidationError("No correct answer")

        validated_questions.append(q)

    return validated_questions