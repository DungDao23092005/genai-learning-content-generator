import streamlit as st
from pydantic import ValidationError

from src.generator import generate_learning_content_raw
from src.output_parser import parse_and_validate_output
from src.schemas import GenerationRequest


# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="GenAI Learning Content Generator",
    page_icon="🧠",
    layout="wide"
)


# =========================
# Session state
# =========================
if "generation_settings" not in st.session_state:
    st.session_state.generation_settings = None

if "generation_started" not in st.session_state:
    st.session_state.generation_started = False

if "raw_generated_output" not in st.session_state:
    st.session_state.raw_generated_output = ""

if "validated_content" not in st.session_state:
    st.session_state.validated_content = None

if "validation_status" not in st.session_state:
    st.session_state.validation_status = ""


# =========================
# Sidebar
# =========================
with st.sidebar:
    st.title("🧠 GenAI Content Generator")

    st.markdown(
        """
        Generate structured learning content from a topic.

        **Main outputs:**
        - Lesson
        - Summary
        - Key points
        - Flashcards
        - Quiz
        - Code exercise
        """
    )

    st.divider()

    st.info(
        "Current stage: JSON parsing and Pydantic validation. "
        "Rendered lesson, quiz, flashcards, and export will be added next."
    )

    st.markdown("### Project Focus")
    st.write("Prompt Engineering")
    st.write("Structured JSON Output")
    st.write("Pydantic Validation")
    st.write("Markdown Export")


# =========================
# Main header
# =========================
st.title("GenAI Quiz & Lesson Content Generator")

st.write(
    "Enter a learning topic and generate structured educational content "
    "such as lessons, quizzes, flashcards, and coding exercises."
)


# =========================
# Input form
# =========================
st.markdown("## Input Settings")

with st.form("content_generation_form"):
    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input(
            "Topic",
            placeholder="Example: Decision Tree, Logistic Regression, SQL Injection"
        )

        level = st.selectbox(
            "Level",
            options=["Beginner", "Intermediate", "Advanced"]
        )

        language = st.selectbox(
            "Language",
            options=["Vietnamese", "English"]
        )

    with col2:
        question_count = st.number_input(
            "Number of quiz questions",
            min_value=3,
            max_value=20,
            value=5,
            step=1
        )

        output_types = st.multiselect(
            "Output types",
            options=[
                "Lesson",
                "Summary",
                "Key Points",
                "Flashcards",
                "Quiz",
                "Code Exercise"
            ],
            default=[
                "Lesson",
                "Summary",
                "Key Points",
                "Flashcards",
                "Quiz",
                "Code Exercise"
            ]
        )

        include_self_review = st.checkbox(
            "Include AI self-review",
            value=True
        )

    learning_objective = st.text_area(
        "Learning objective",
        placeholder=(
            "Example: Help beginners understand the core idea, "
            "important formulas, and common use cases."
        ),
        height=100
    )

    submitted = st.form_submit_button(
        "Generate Content",
        type="primary"
    )


# =========================
# Handle form submission
# =========================
if submitted:
    if not topic.strip():
        st.error("Please enter a topic before generating content.")
    elif not output_types:
        st.error("Please select at least one output type.")
    else:
        try:
            generation_request = GenerationRequest(
                topic=topic.strip(),
                level=level,
                language=language,
                question_count=int(question_count),
                output_types=output_types,
                learning_objective=learning_objective.strip(),
                include_self_review=include_self_review,
            )

            st.session_state.generation_settings = generation_request.model_dump()
            st.session_state.generation_started = True
            st.session_state.raw_generated_output = ""
            st.session_state.validated_content = None
            st.session_state.validation_status = ""

            with st.spinner("Generating learning content with Gemini..."):
                raw_output = generate_learning_content_raw(generation_request)

            st.session_state.raw_generated_output = raw_output

            with st.spinner("Parsing and validating JSON output..."):
                validated_content = parse_and_validate_output(raw_output)

            st.session_state.validated_content = validated_content.model_dump()
            st.session_state.validation_status = "success"

            st.success("Learning content generated and validated successfully.")

        except ValidationError as error:
            st.session_state.validation_status = "failed"
            st.error(f"Invalid input settings: {error}")

        except Exception as error:
            st.session_state.validation_status = "failed"
            st.error(f"Failed to generate or validate content: {error}")


# =========================
# Preview generation settings
# =========================
if st.session_state.generation_settings:
    st.markdown("## Current Generation Settings")

    settings = st.session_state.generation_settings

    col_a, col_b, col_c, col_d = st.columns(4)

    col_a.metric("Topic", settings["topic"])
    col_b.metric("Level", settings["level"])
    col_c.metric("Language", settings["language"])
    col_d.metric("Questions", settings["question_count"])

    st.markdown("### Selected Output Types")
    st.write(", ".join(settings["output_types"]))

    if settings["learning_objective"]:
        st.markdown("### Learning Objective")
        st.write(settings["learning_objective"])

    st.markdown("### Raw Settings Preview")
    st.json(settings)


# =========================
# Output preview tabs
# =========================
st.markdown("## Generated Output Preview")

lesson_tab, quiz_tab, flashcard_tab, code_tab, review_tab, raw_tab = st.tabs(
    [
        "📘 Lesson",
        "❓ Quiz",
        "🧩 Flashcards",
        "💻 Code Exercise",
        "✅ Self Review",
        "🧾 Raw JSON"
    ]
)


# =========================
# Lesson tab
# =========================
with lesson_tab:
    st.subheader("Lesson Output")

    if st.session_state.validated_content:
        content = st.session_state.validated_content

        st.markdown(f"### {content['lesson_title']}")
        st.info(
            "Content is already parsed and validated. "
            "A better UI renderer will be added in the next commit."
        )

        lesson_preview = content["lesson"]

        if len(lesson_preview) > 1000:
            lesson_preview = lesson_preview[:1000] + "..."

        st.write(lesson_preview)

    elif st.session_state.generation_started:
        st.info("Validated lesson preview will appear here after generation.")
    else:
        st.write("Submit the form to start content generation.")


# =========================
# Quiz tab
# =========================
with quiz_tab:
    st.subheader("Quiz Output")

    if st.session_state.validated_content:
        content = st.session_state.validated_content

        st.success(
            f"Validated {len(content['quiz'])} quiz questions successfully."
        )

        st.write(
            "Detailed quiz rendering will be added in the next commit."
        )

    elif st.session_state.generation_started:
        st.info("Validated quiz questions will appear here after generation.")
    else:
        st.write("Submit the form to start content generation.")


# =========================
# Flashcards tab
# =========================
with flashcard_tab:
    st.subheader("Flashcards Output")

    if st.session_state.validated_content:
        content = st.session_state.validated_content

        st.success(
            f"Validated {len(content['flashcards'])} flashcards successfully."
        )

        st.write(
            "Detailed flashcard rendering will be added in the next commit."
        )

    elif st.session_state.generation_started:
        st.info("Validated flashcards will appear here after generation.")
    else:
        st.write("Submit the form to start content generation.")


# =========================
# Code Exercise tab
# =========================
with code_tab:
    st.subheader("Code Exercise Output")

    if st.session_state.validated_content:
        content = st.session_state.validated_content
        code_exercise = content.get("code_exercise")

        if code_exercise:
            st.success("Validated code exercise successfully.")
            st.write(
                "Detailed code exercise rendering will be added in the next commit."
            )
        else:
            st.warning("No code exercise was generated.")

    elif st.session_state.generation_started:
        st.info("Validated code exercise will appear here after generation.")
    else:
        st.write("Submit the form to start content generation.")


# =========================
# Self Review tab
# =========================
with review_tab:
    st.subheader("AI Self Review")

    if st.session_state.validated_content:
        content = st.session_state.validated_content
        self_review = content.get("self_review")

        if self_review:
            st.success(
                f"Self-review quality score: "
                f"{self_review['quality_score']} / 10"
            )
        else:
            st.warning("Self-review is disabled or not generated.")

    elif st.session_state.generation_started:
        st.info("Validated self-review will appear here after generation.")
    else:
        st.write("Submit the form to start content generation.")


# =========================
# Raw JSON tab
# =========================
with raw_tab:
    st.subheader("Raw Gemini Output")

    if st.session_state.raw_generated_output:
        st.code(
            st.session_state.raw_generated_output,
            language="json"
        )
    else:
        st.write("Raw JSON output will appear here after generation.")

    st.divider()

    st.subheader("Validated Pydantic Output")

    if st.session_state.validated_content:
        st.success("Output passed Pydantic validation.")
        st.json(st.session_state.validated_content)
    elif st.session_state.validation_status == "failed":
        st.error("Output validation failed.")
    else:
        st.write("Validated output will appear here after generation.")