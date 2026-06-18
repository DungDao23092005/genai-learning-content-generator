# GenAI Learning Content Generator

GenAI Learning Content Generator is a personal AI project that helps generate learning materials from a given topic using Generative AI.

Users can enter a topic, select a difficulty level, choose the number of quiz questions, and generate structured learning content such as lesson notes, key points, flashcards, quizzes, answers, explanations, and small Python coding exercises.

This project was built as a portfolio project for AI Engineer / Machine Learning Engineer internship applications.

---

## Demo Features

* Enter a learning topic
* Select difficulty level: Beginner, Intermediate, Advanced
* Select number of quiz questions
* Select output language: Vietnamese or English
* Generate lesson content
* Generate key points
* Generate flashcards
* Generate multiple-choice quizzes
* Generate answers and explanations
* Generate small Python coding exercises
* Validate structured JSON output using Pydantic
* Export generated content as Markdown

---

## Tech Stack

* Python
* Streamlit
* Gemini API
* Pydantic
* JSON parsing
* Markdown export

---

## Project Architecture

```text
User enters topic and settings
        ↓
Build prompt using prompt templates
        ↓
Send prompt to Gemini API
        ↓
Receive structured JSON output
        ↓
Parse JSON response
        ↓
Validate output using Pydantic schema
        ↓
Render lesson, quiz, flashcards, and code exercise
        ↓
Export result as Markdown
```

---

## Folder Structure

```text
genai-learning-content-generator/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── prompt_templates.py
│   ├── generator.py
│   ├── output_parser.py
│   ├── export_utils.py
│   └── schemas.py
│
├── examples/
│   ├── decision_tree_lesson.md
│   └── logistic_regression_quiz.md
│
└── screenshots/
```

---

## Prompt Engineering Techniques

This project demonstrates several prompt engineering techniques:

* Role prompting
* Structured JSON output
* Difficulty control
* Language control
* Self-checking prompt
* Output validation with Pydantic
* Clear task decomposition
* Consistent output formatting

---

## Example Input

```text
Topic: Logistic Regression
Difficulty Level: Beginner
Number of Questions: 5
Language: English
Output Type: Lesson + Quiz + Flashcards + Code Exercise
```

---

## Example Output

The app generates structured learning content including:

```text
Lesson:
A short explanation of the selected topic.

Key Points:
Important concepts that learners should remember.

Flashcards:
Question-answer pairs for quick revision.

Quiz:
Multiple-choice questions with four options.

Answers:
Correct answers for each question.

Explanations:
Simple explanations for why each answer is correct.

Coding Exercise:
A small Python exercise related to the topic.
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/DungDao23092005/genai-learning-content-generator.git
```

```bash
cd genai-learning-content-generator
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

---

### 3. Activate the virtual environment

On Windows CMD:

```bash
.venv\Scripts\activate
```

On Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```bash
.\.venv\Scripts\Activate.ps1
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Create `.env` file

```bash
copy .env.example .env
```

Then open `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 6. Run the Streamlit app

```bash
streamlit run app.py
```

---

## Environment Variables

Create a `.env` file in the root folder and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit your `.env` file to GitHub.

---

## Example `requirements.txt`

```txt
streamlit
python-dotenv
google-genai
pydantic
```

---

## Core Modules

### `prompt_templates.py`

Contains prompt templates used to instruct the AI model to generate structured learning content.

### `generator.py`

Handles communication with the Gemini API and sends prompts to the model.

### `output_parser.py`

Parses the raw model response and converts it into valid JSON.

### `schemas.py`

Defines Pydantic models for validating lesson content, flashcards, quizzes, answers, explanations, and coding exercises.

### `export_utils.py`

Exports the generated learning content into Markdown format.

### `app.py`

Main Streamlit application file that connects the UI with the content generation pipeline.

---

## Screenshots

Add screenshots of the app inside the `screenshots/` folder.

Example:

```text
screenshots/
│
├── home_page.png
├── generated_lesson.png
├── quiz_output.png
└── markdown_export.png
```

Then display them in this README:

```md
## Screenshots

### Home Page

![Home Page](screenshots/home_page.png)

### Generated Lesson

![Generated Lesson](screenshots/generated_lesson.png)

### Quiz Output

![Quiz Output](screenshots/quiz_output.png)
```

---

## Project Status

This project is under development.

Current progress:

* Project structure created
* README prepared
* Prompt design planned
* Streamlit UI planned
* Gemini API integration planned
* Pydantic schema validation planned
* Markdown export planned

---

## Future Improvements

* Add support for more output formats
* Add PDF export
* Add DOCX export
* Add quiz difficulty analysis
* Add lesson history
* Add downloadable flashcard deck
* Add support for more AI models
* Improve JSON parsing error handling
* Deploy the app online

---

## Author

**DungDao23092005**

* GitHub: `DungDao23092005`
* LinkedIn: `dungdao2309`

---

## License

This project is for learning and portfolio purposes.
