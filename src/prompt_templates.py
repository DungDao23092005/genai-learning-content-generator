from src.schemas import GenerationRequest


def build_learning_content_prompt(request: GenerationRequest) -> str:
    """
    Build a prompt that asks Gemini to generate structured learning content.

    The output must be valid JSON so it can be parsed and validated
    with Pydantic later.
    """
    output_types_text = ", ".join(request.output_types)

    learning_objective = (
        request.learning_objective
        if request.learning_objective
        else "Help learners understand the topic clearly and practically."
    )

    self_review_instruction = (
        """
Also include a self_review object with:
- quality_score from 1 to 10
- strengths
- weaknesses
- improvement_suggestions
"""
        if request.include_self_review
        else """
Set self_review to null.
"""
    )

    prompt = f"""
You are an expert AI learning content creator.

Your task is to generate structured educational content for students.

User settings:
- Topic: {request.topic}
- Difficulty level: {request.level}
- Language: {request.language}
- Number of quiz questions: {request.question_count}
- Requested output types: {output_types_text}
- Learning objective: {learning_objective}

Prompt engineering requirements:
1. Use role prompting: act as a clear and helpful AI tutor.
2. Use difficulty control: adapt explanation depth to {request.level} level.
3. Use language control: write all learner-facing content in {request.language}.
4. Use structured JSON output only.
5. Do not include markdown fences.
6. Do not include extra text outside JSON.
7. Generate exactly {request.question_count} quiz questions.
8. Each quiz question must have exactly 4 options: A, B, C, D.
9. The correct answer must be one of: A, B, C, D.
10. Include explanations for all quiz answers.
11. Include practical examples when helpful.
12. Include a small Python coding exercise related to the topic if possible.
13. Make sure the content is accurate, beginner-friendly when level is Beginner, and more technical when level is Advanced.

Self-review instruction:
{self_review_instruction}

Return ONLY valid JSON in this exact structure:

{{
  "lesson_title": "A clear title for the lesson",
  "lesson": "A structured lesson explanation written as plain text",
  "summary": "A short summary of the lesson",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ],
  "flashcards": [
    {{
      "term": "Important term",
      "definition": "Clear definition"
    }}
  ],
  "quiz": [
    {{
      "question": "Question text",
      "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      }},
      "answer": "A",
      "explanation": "Explanation for why the answer is correct"
    }}
  ],
  "code_exercise": {{
    "title": "Exercise title",
    "description": "Exercise description",
    "starter_code": "Python starter code",
    "expected_output": "Expected output or expected behavior",
    "solution": "Python solution code",
    "explanation": "Explanation of the solution"
  }},
  "self_review": {{
    "quality_score": 8,
    "strengths": [
      "Strength 1",
      "Strength 2"
    ],
    "weaknesses": [
      "Weakness 1"
    ],
    "improvement_suggestions": [
      "Suggestion 1"
    ]
  }}
}}

Important:
- The JSON must be parseable by Python json.loads().
- Do not wrap the JSON in ```json.
- Do not add comments inside JSON.
- Use double quotes for all JSON keys and string values.
"""
    return prompt.strip()


def build_repair_json_prompt(raw_output: str, validation_error: str) -> str:
    """
    Build a prompt to repair invalid JSON or invalid schema output.

    This will be used later if Gemini returns malformed JSON.
    """
    prompt = f"""
You are a JSON repair assistant.

The following AI output is invalid or does not match the required schema.

Invalid output:
{raw_output}

Validation error:
{validation_error}

Your task:
1. Fix the output into valid JSON.
2. Keep the original meaning as much as possible.
3. Ensure all required fields are present.
4. Ensure quiz options contain exactly A, B, C, and D.
5. Ensure answer is one of A, B, C, or D.
6. Return ONLY valid JSON.
7. Do not include markdown fences.
8. Do not include explanations outside JSON.

Return the fixed JSON only.
"""
    return prompt.strip()


def build_self_check_prompt(validated_content_json: str) -> str:
    """
    Build a self-checking prompt for reviewing generated content quality.
    """
    prompt = f"""
You are an AI content quality reviewer.

Review the following generated learning content.

Content JSON:
{validated_content_json}

Check for:
1. Accuracy
2. Clarity
3. Difficulty level consistency
4. Quiz quality
5. Explanation quality
6. Code exercise usefulness

Return ONLY valid JSON in this format:

{{
  "quality_score": 8,
  "strengths": [
    "Strength 1",
    "Strength 2"
  ],
  "weaknesses": [
    "Weakness 1"
  ],
  "improvement_suggestions": [
    "Suggestion 1"
  ]
}}
"""
    return prompt.strip()