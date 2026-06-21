from datetime import datetime

import streamlit as st
from pydantic import ValidationError

from src.export_utils import (
    build_markdown_filename,
    export_learning_content_to_markdown,
)
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

if "markdown_output" not in st.session_state:
    st.session_state.markdown_output = ""

if "markdown_filename" not in st.session_state:
    st.session_state.markdown_filename = "generated_learning_content.md"

if "generation_history" not in st.session_state:
    st.session_state.generation_history = []


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
        "Current stage: rendered learning content, quiz, flashcards, "
        "self-review, raw JSON preview, Markdown export, and session history."
    )

    st.markdown("### Project Focus")
    st.write("Prompt Engineering")
    st.write("Structured JSON Output")
    st.write("Pydantic Validation")
    st.write("Markdown Export")
    st.write("Session History")

    st.divider()

    st.markdown("### Session Stats")
    st.metric(
        "Generated items",
        len(st.session_state.generation_history)
    )


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

            # Reset previous outputs before generating new content
            st.session_state.raw_generated_output = ""
            st.session_state.validated_content = None
            st.session_state.validation_status = ""
            st.session_state.markdown_output = ""
            st.session_state.markdown_filename = "generated_learning_content.md"

            with st.spinner("Generating learning content with Gemini..."):
                raw_output = generate_learning_content_raw(generation_request)

            st.session_state.raw_generated_output = raw_output

            with st.spinner("Parsing and validating JSON output..."):
                validated_content = parse_and_validate_output(raw_output)

            validated_content_dict = validated_content.model_dump()

            st.session_state.validated_content = validated_content_dict
            st.session_state.validation_status = "success"

            markdown_output = export_learning_content_to_markdown(
                content=validated_content_dict,
                settings=st.session_state.generation_settings
            )

            markdown_filename = build_markdown_filename(validated_content_dict)

            st.session_state.markdown_output = markdown_output
            st.session_state.markdown_filename = markdown_filename

            history_item = {
                "id": len(st.session_state.generation_history) + 1,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "topic": st.session_state.generation_settings["topic"],
                "level": st.session_state.generation_settings["level"],
                "language": st.session_state.generation_settings["language"],
                "question_count": st.session_state.generation_settings["question_count"],
                "lesson_title": validated_content_dict["lesson_title"],
                "markdown_filename": markdown_filename,
                "markdown_output": markdown_output,
            }

            st.session_state.generation_history.append(history_item)

            st.success(
                "Learning content generated, validated, exported, and saved to history."
            )

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
# Helper render functions
# =========================
def get_validated_content():
    """
    Get validated content from Streamlit session state.
    """
    return st.session_state.validated_content


def render_empty_state(message: str) -> None:
    """
    Render a simple empty state message.
    """
    if st.session_state.generation_started:
        st.info(message)
    else:
        st.write("Submit the form to start content generation.")


# =========================
# Output preview tabs
# =========================
st.markdown("## Generated Output Preview")

lesson_tab, quiz_tab, flashcard_tab, code_tab, review_tab, export_tab, history_tab, raw_tab = st.tabs(
    [
        "📘 Lesson",
        "❓ Quiz",
        "🧩 Flashcards",
        "💻 Code Exercise",
        "✅ Self Review",
        "📤 Export",
        "🕘 History",
        "🧾 Raw JSON"
    ]
)


# =========================
# Lesson tab
# =========================
with lesson_tab:
    st.subheader("Lesson Output")

    content = get_validated_content()

    if content:
        st.markdown(f"## {content['lesson_title']}")

        st.markdown("### Summary")
        st.write(content["summary"])

        st.markdown("### Lesson")
        st.write(content["lesson"])

        st.markdown("### Key Points")
        for index, point in enumerate(content["key_points"], start=1):
            st.markdown(f"{index}. {point}")

    else:
        render_empty_state("Validated lesson will appear here after generation.")


# =========================
# Quiz tab
# =========================
with quiz_tab:
    st.subheader("Quiz Output")

    content = get_validated_content()

    if content:
        quiz_questions = content["quiz"]

        st.success(f"Generated {len(quiz_questions)} quiz questions.")

        for index, question in enumerate(quiz_questions, start=1):
            st.markdown(f"### Question {index}")
            st.write(question["question"])

            options = question["options"]

            selected_answer = st.radio(
                "Choose your answer:",
                options=["A", "B", "C", "D"],
                format_func=lambda option, opts=options: (
                    f"{option}. {opts.get(option, '')}"
                ),
                key=f"quiz_answer_{index}"
            )

            with st.expander("Show answer and explanation"):
                correct_answer = question["answer"]

                if selected_answer == correct_answer:
                    st.success(f"Correct answer: {correct_answer}")
                else:
                    st.error(
                        f"Your answer: {selected_answer} | "
                        f"Correct answer: {correct_answer}"
                    )

                st.write(f"**Explanation:** {question['explanation']}")

            st.divider()

    else:
        render_empty_state("Validated quiz questions will appear here after generation.")


# =========================
# Flashcards tab
# =========================
with flashcard_tab:
    st.subheader("Flashcards Output")

    content = get_validated_content()

    if content:
        flashcards = content["flashcards"]

        st.success(f"Generated {len(flashcards)} flashcards.")

        for index, card in enumerate(flashcards, start=1):
            with st.expander(f"Flashcard {index}: {card['term']}"):
                st.write(card["definition"])

    else:
        render_empty_state("Validated flashcards will appear here after generation.")


# =========================
# Code Exercise tab
# =========================
with code_tab:
    st.subheader("Code Exercise Output")

    content = get_validated_content()

    if content:
        code_exercise = content.get("code_exercise")

        if code_exercise:
            st.markdown(f"### {code_exercise['title']}")

            st.markdown("### Description")
            st.write(code_exercise["description"])

            st.markdown("### Starter Code")
            st.code(
                code_exercise["starter_code"],
                language="python"
            )

            if code_exercise.get("expected_output"):
                st.markdown("### Expected Output")
                st.code(
                    code_exercise["expected_output"],
                    language="text"
                )

            with st.expander("Show solution"):
                if code_exercise.get("solution"):
                    st.code(
                        code_exercise["solution"],
                        language="python"
                    )

                if code_exercise.get("explanation"):
                    st.markdown("### Explanation")
                    st.write(code_exercise["explanation"])

        else:
            st.warning("No code exercise was generated.")

    else:
        render_empty_state("Validated code exercise will appear here after generation.")


# =========================
# Self Review tab
# =========================
with review_tab:
    st.subheader("AI Self Review")

    content = get_validated_content()

    if content:
        self_review = content.get("self_review")

        if self_review:
            st.metric(
                "Quality Score",
                f"{self_review['quality_score']} / 10"
            )

            st.markdown("### Strengths")
            for item in self_review["strengths"]:
                st.markdown(f"- {item}")

            st.markdown("### Weaknesses")
            for item in self_review["weaknesses"]:
                st.markdown(f"- {item}")

            st.markdown("### Improvement Suggestions")
            for item in self_review["improvement_suggestions"]:
                st.markdown(f"- {item}")

        else:
            st.warning("Self-review is disabled or not generated.")

    else:
        render_empty_state("Validated self-review will appear here after generation.")


# =========================
# Export tab
# =========================
with export_tab:
    st.subheader("Export Markdown")

    if st.session_state.markdown_output:
        st.success("Markdown export is ready.")

        st.download_button(
            label="Download Markdown",
            data=st.session_state.markdown_output,
            file_name=st.session_state.markdown_filename,
            mime="text/markdown",
            type="primary"
        )

        st.markdown("### Markdown Preview")
        st.code(
            st.session_state.markdown_output,
            language="markdown"
        )

    else:
        render_empty_state("Markdown export will appear here after generation.")


# =========================
# History tab
# =========================
with history_tab:
    st.subheader("Generation History")

    if st.session_state.generation_history:
        st.success(
            f"{len(st.session_state.generation_history)} generated item(s) in this session."
        )

        history_options = list(reversed(st.session_state.generation_history))

        selected_label = st.selectbox(
            "Select a generated item",
            options=[
                f"#{item['id']} | {item['topic']} | {item['level']} | {item['created_at']}"
                for item in history_options
            ]
        )

        selected_index = [
            f"#{item['id']} | {item['topic']} | {item['level']} | {item['created_at']}"
            for item in history_options
        ].index(selected_label)

        selected_item = history_options[selected_index]

        st.markdown("### Selected Item")

        col_h1, col_h2, col_h3, col_h4 = st.columns(4)

        col_h1.metric("Topic", selected_item["topic"])
        col_h2.metric("Level", selected_item["level"])
        col_h3.metric("Language", selected_item["language"])
        col_h4.metric("Questions", selected_item["question_count"])

        st.markdown(f"**Lesson title:** {selected_item['lesson_title']}")
        st.markdown(f"**Created at:** {selected_item['created_at']}")

        st.download_button(
            label="Download Selected Markdown",
            data=selected_item["markdown_output"],
            file_name=selected_item["markdown_filename"],
            mime="text/markdown",
            key=f"download_history_{selected_item['id']}",
            type="primary"
        )

        with st.expander("Preview selected Markdown"):
            st.code(
                selected_item["markdown_output"],
                language="markdown"
            )

        if st.button("Clear History"):
            st.session_state.generation_history = []
            st.rerun()

    else:
        st.info("No generation history yet. Generate content to see it here.")


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