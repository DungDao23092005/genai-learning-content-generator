import json
import re
from json import JSONDecodeError
from typing import Any, Dict

from pydantic import ValidationError

from src.generator import generate_text_with_fallback
from src.prompt_templates import build_repair_json_prompt
from src.schemas import LearningContent


def clean_json_text(raw_text: str) -> str:
    """
    Clean Gemini raw output before JSON parsing.

    Gemini may return JSON inside markdown fences like:
    ```json
    {...}
    ```
    This function removes markdown fences and keeps only the JSON object.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Raw output is empty.")

    cleaned = raw_text.strip()

    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace == -1 or last_brace == -1:
        raise ValueError("No JSON object found in raw output.")

    cleaned = cleaned[first_brace:last_brace + 1]

    return cleaned.strip()


def parse_json_output(raw_text: str) -> Dict[str, Any]:
    """
    Parse raw Gemini output into a Python dictionary.
    """
    cleaned_text = clean_json_text(raw_text)

    return json.loads(cleaned_text)


def validate_learning_content(data: Dict[str, Any]) -> LearningContent:
    """
    Validate parsed JSON using the LearningContent Pydantic schema.
    """
    return LearningContent.model_validate(data)


def parse_and_validate_output(raw_text: str) -> LearningContent:
    """
    Parse and validate Gemini output.

    If parsing or validation fails, use a JSON repair prompt once,
    then try parsing and validation again.
    """
    try:
        parsed_data = parse_json_output(raw_text)
        validated_content = validate_learning_content(parsed_data)

        return validated_content

    except (JSONDecodeError, ValidationError, ValueError) as error:
        repair_prompt = build_repair_json_prompt(
            raw_output=raw_text,
            validation_error=str(error)
        )

        repaired_output = generate_text_with_fallback(repair_prompt)

        parsed_data = parse_json_output(repaired_output)
        validated_content = validate_learning_content(parsed_data)

        return validated_content