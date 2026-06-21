from datetime import datetime
from typing import Dict, List


def slugify_filename(text: str) -> str:
    """
    Convert a text into a safe filename.
    """
    safe_text = text.lower().strip()

    replacements = {
        " ": "_",
        "/": "_",
        "\\": "_",
        ":": "_",
        "*": "_",
        "?": "_",
        "\"": "_",
        "<": "_",
        ">": "_",
        "|": "_",
    }

    for old, new in replacements.items():
        safe_text = safe_text.replace(old, new)

    safe_text = "".join(
        char for char in safe_text
        if char.isalnum() or char in ["_", "-"]
    )

    return safe_text or "generated_learning_content"


def format_key_points(key_points: List[str]) -> str:
    """
    Format key points as Markdown bullet list.
    """
    lines = []

    for point in key_points:
        lines.append(f"- {point}")

    return "\n".join(lines)


def format_flashcards(flashcards: List[Dict]) -> str:
    """
    Format flashcards as Markdown.
    """
    lines = []

    for index, card in enumerate(flashcards, start=1):
        lines.append(f"### Flashcard {index}: {card['term']}")
        lines.append("")
        lines.append(f"**Definition:** {card['definition']}")
        lines.append("")

    return "\n".join(lines)


def format_quiz(quiz_questions: List[Dict]) -> str:
    """
    Format quiz questions as Markdown.
    """
    lines = []

    for index, question in enumerate(quiz_questions, start=1):
        lines.append(f"### Question {index}")
        lines.append("")
        lines.append(question["question"])
        lines.append("")

        options = question["options"]

        for option_key in ["A", "B", "C", "D"]:
            lines.append(f"- **{option_key}.** {options.get(option_key, '')}")

        lines.append("")
        lines.append(f"**Answer:** {question['answer']}")
        lines.append("")
        lines.append(f"**Explanation:** {question['explanation']}")
        lines.append("")

    return "\n".join(lines)


def format_code_exercise(code_exercise: Dict | None) -> str:
    """
    Format code exercise as Markdown.
    """
    if not code_exercise:
        return "No code exercise was generated."

    lines = []

    lines.append(f"### {code_exercise['title']}")
    lines.append("")
    lines.append("**Description:**")
    lines.append("")
    lines.append(code_exercise["description"])
    lines.append("")

    lines.append("**Starter Code:**")
    lines.append("")
    lines.append("```python")
    lines.append(code_exercise["starter_code"])
    lines.append("```")
    lines.append("")

    if code_exercise.get("expected_output"):
        lines.append("**Expected Output:**")
        lines.append("")
        lines.append("```text")
        lines.append(code_exercise["expected_output"])
        lines.append("```")
        lines.append("")

    if code_exercise.get("solution"):
        lines.append("**Solution:**")
        lines.append("")
        lines.append("```python")
        lines.append(code_exercise["solution"])
        lines.append("```")
        lines.append("")

    if code_exercise.get("explanation"):
        lines.append("**Explanation:**")
        lines.append("")
        lines.append(code_exercise["explanation"])
        lines.append("")

    return "\n".join(lines)


def format_self_review(self_review: Dict | None) -> str:
    """
    Format AI self-review as Markdown.
    """
    if not self_review:
        return "No self-review was generated."

    lines = []

    lines.append(f"**Quality Score:** {self_review['quality_score']} / 10")
    lines.append("")

    lines.append("### Strengths")
    for item in self_review["strengths"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("### Weaknesses")
    for item in self_review["weaknesses"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("### Improvement Suggestions")
    for item in self_review["improvement_suggestions"]:
        lines.append(f"- {item}")

    return "\n".join(lines)


def export_learning_content_to_markdown(
    content: Dict,
    settings: Dict | None = None
) -> str:
    """
    Convert validated learning content into Markdown.
    """
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []

    lines.append(f"# {content['lesson_title']}")
    lines.append("")
    lines.append(f"Generated at: `{generated_at}`")
    lines.append("")

    if settings:
        lines.append("## Generation Settings")
        lines.append("")
        lines.append(f"- **Topic:** {settings.get('topic', '')}")
        lines.append(f"- **Level:** {settings.get('level', '')}")
        lines.append(f"- **Language:** {settings.get('language', '')}")
        lines.append(f"- **Question Count:** {settings.get('question_count', '')}")
        lines.append(
            f"- **Output Types:** {', '.join(settings.get('output_types', []))}"
        )

        if settings.get("learning_objective"):
            lines.append(
                f"- **Learning Objective:** {settings.get('learning_objective')}"
            )

        lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(content["summary"])
    lines.append("")

    lines.append("## Lesson")
    lines.append("")
    lines.append(content["lesson"])
    lines.append("")

    lines.append("## Key Points")
    lines.append("")
    lines.append(format_key_points(content["key_points"]))
    lines.append("")

    lines.append("## Flashcards")
    lines.append("")
    lines.append(format_flashcards(content["flashcards"]))
    lines.append("")

    lines.append("## Quiz")
    lines.append("")
    lines.append(format_quiz(content["quiz"]))
    lines.append("")

    lines.append("## Code Exercise")
    lines.append("")
    lines.append(format_code_exercise(content.get("code_exercise")))
    lines.append("")

    lines.append("## AI Self Review")
    lines.append("")
    lines.append(format_self_review(content.get("self_review")))
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "Generated by GenAI Learning Content Generator."
    )

    return "\n".join(lines)


def build_markdown_filename(content: Dict) -> str:
    """
    Build a Markdown filename from lesson title.
    """
    base_name = slugify_filename(content["lesson_title"])

    return f"{base_name}.md"