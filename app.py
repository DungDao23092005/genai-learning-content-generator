import streamlit as st


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
        "Current stage: UI input form. "
        "Gemini generation and JSON validation will be added later."
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
        st.session_state.generation_settings = {
            "topic": topic.strip(),
            "level": level,
            "language": language,
            "question_count": int(question_count),
            "output_types": output_types,
            "learning_objective": learning_objective.strip(),
            "include_self_review": include_self_review,
        }

        st.session_state.generation_started = True

        st.success("Input settings saved. AI generation will be added in a later commit.")


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

lesson_tab, quiz_tab, flashcard_tab, code_tab, review_tab = st.tabs(
    [
        "📘 Lesson",
        "❓ Quiz",
        "🧩 Flashcards",
        "💻 Code Exercise",
        "✅ Self Review"
    ]
)

with lesson_tab:
    st.subheader("Lesson Output")
    if st.session_state.generation_started:
        st.info("Generated lesson will appear here in a later commit.")
    else:
        st.write("Submit the form to start content generation.")

with quiz_tab:
    st.subheader("Quiz Output")
    if st.session_state.generation_started:
        st.info("Generated quiz questions will appear here in a later commit.")
    else:
        st.write("Submit the form to start content generation.")

with flashcard_tab:
    st.subheader("Flashcards Output")
    if st.session_state.generation_started:
        st.info("Generated flashcards will appear here in a later commit.")
    else:
        st.write("Submit the form to start content generation.")

with code_tab:
    st.subheader("Code Exercise Output")
    if st.session_state.generation_started:
        st.info("Generated Python coding exercise will appear here in a later commit.")
    else:
        st.write("Submit the form to start content generation.")

with review_tab:
    st.subheader("AI Self Review")
    if st.session_state.generation_started:
        if st.session_state.generation_settings["include_self_review"]:
            st.info("AI self-review will appear here in a later commit.")
        else:
            st.warning("Self-review is disabled.")
    else:
        st.write("Submit the form to start content generation.")