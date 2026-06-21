import os
from typing import List

from dotenv import load_dotenv
from google import genai

from src.prompt_templates import build_learning_content_prompt
from src.schemas import GenerationRequest


GENERATION_MODELS: List[str] = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


def get_gemini_client() -> genai.Client:
    """
    Create a Gemini client using GOOGLE_API_KEY from .env.
    """
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is missing. Please create a .env file "
            "and add your Gemini API key."
        )

    return genai.Client(api_key=api_key)


def generate_text_with_fallback(prompt: str) -> str:
    """
    Generate text using Gemini with fallback models.

    If the first model fails, the function tries the next model.
    """
    client = get_gemini_client()
    last_error = None

    for model_name in GENERATION_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception as error:
            last_error = error

    raise RuntimeError(
        "Failed to generate content with all fallback models. "
        f"Last error: {last_error}"
    )


def generate_learning_content_raw(request: GenerationRequest) -> str:
    """
    Generate raw structured learning content as text.

    At this stage, the output is still raw JSON text.
    It will be parsed and validated in the next commit.
    """
    prompt = build_learning_content_prompt(request)

    raw_output = generate_text_with_fallback(prompt)

    return raw_output