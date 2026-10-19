## StudyMate AI 📚

**An AI-powered study planner and quiz generator built with Python and Streamlit.**

## Overview

StudyMate AI is a student-focused application designed to help organize exam preparation. It uses AI to assist with study planning and quiz generation, helping students structure their learning around their syllabus and available preparation time.

## Features

- Personalized Study Planning: Generate day-by-day study schedules based on subjects, exam dates, and daily study hours.
- AI-Powered Quizzes: Generate five-question, topic-specific multiple-choice quizzes using the Google Gemini API.
- PDF Syllabus Support: Extract syllabus text from uploaded PDF files using PyPDF.
- Database Storage: Save generated study plans in an SQLite database.
- Study Plan Export: Download generated study plans as text files.
- Interactive Interface:  Use a Streamlit interface with separate study planner and quiz generator tabs.

- 
## Tech Stack

- Python
- Streamlit
- Google Gemini API
- SQLite
- PyPDF

## Getting Started

 1. Clone the repository

```bash
git clone https://github.com/khushiydv12/studymate-ai.git
cd studymate-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

Set up your Google Gemini API key using the configuration expected by the application. Do not commit API keys or other secrets to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

## Project Goals

- Make study planning more organized and accessible.
- Help students practise through AI-generated quizzes.
- Reduce the effort involved in organizing syllabus-based preparation.

## Future Improvements

- Progress tracking and study analytics.
- More flexible scheduling options.
- Additional quiz customization.
- Improved study recommendations.

## Author

**Khushi Yadav**

- GitHub: [@khushiydv12](https://github.com/khushiydv12)
