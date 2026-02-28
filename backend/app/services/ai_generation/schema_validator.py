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

        # Required keys that MUST be present
        required_keys = [
            "question_text",
            "options",
        ]

        for key in required_keys:
            if key not in q:
                raise SchemaValidationError(f"Missing required key: {key}")

        if not isinstance(q["question_text"], str):
            raise SchemaValidationError("question_text must be string")

        if not isinstance(q["options"], list):
            raise SchemaValidationError("options must be list")

        if len(q["options"]) < 4:
            raise SchemaValidationError("Less than 4 options")

        # Validate options have required structure
        for option in q["options"]:
            if not isinstance(option.get("id"), str):
                raise SchemaValidationError("Option id must be string")
            if not isinstance(option.get("text"), str):
                raise SchemaValidationError("Option text must be string")
            if not isinstance(option.get("is_correct"), bool):
                raise SchemaValidationError("is_correct must be bool")

        # Check at least one correct answer
        correct_count = sum(1 for opt in q["options"] if opt.get("is_correct", False))
        if correct_count < 1:
            raise SchemaValidationError("No correct answer found")

        # Set defaults for optional fields
        q.setdefault("question_id", f"q_{len(validated_questions)}")
        q.setdefault("topic", "General")
        q.setdefault("difficulty", "medium")
        q.setdefault("question_type", "single")
        q.setdefault("multiple_selectable", False)
        q.setdefault("concept_tags", ["General"])
        q.setdefault("base_explanation", "")

        # Validate optional fields when present
        if q.get("difficulty") not in ["easy", "medium", "hard"]:
            q["difficulty"] = "medium"

        if q.get("question_type") not in ["single", "multiple"]:
            q["question_type"] = "single"

        if not isinstance(q.get("multiple_selectable"), bool):
            q["multiple_selectable"] = False

        if not isinstance(q.get("concept_tags"), list):
            q["concept_tags"] = ["General"]

        validated_questions.append(q)

    return validated_questions

def validate_explanation(parsed: dict) -> str:
    if not isinstance(parsed, dict):
        raise SchemaValidationError("Root must be object")
    if "adaptive_explanation" not in parsed:
        raise SchemaValidationError("Missing 'adaptive_explanation' key")
    if not isinstance(parsed["adaptive_explanation"], str):
        raise SchemaValidationError("adaptive_explanation must be string")
    return parsed["adaptive_explanation"]