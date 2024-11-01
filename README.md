# GPT Experiments

## Overview

**GPT Experiments** is a Flask-based project that I work on in my free time to develop my skills in working with LLMs (Large Language Models) and Generative AI. This project explores various implementations of chatbots using OpenAI's API, alongside a CV extractor for processing document files. It currently features three distinct chatbots, each with unique functionalities, and a tool for extracting information from CVs in PDF or Word formats.

## Table of Contents

- [Features](#features)
- [Installation](#installation)

## Features

- Three chatbots with different capabilities:
  - **Basic Chatbot:** A simple conversational agent with memory and history tracking for unique sessions.
  - **SQLite Chatbot:** Similar to the basic chatbot, but it stores conversation history in an SQLite database.
  - **Database Query Chatbot:** Connects to a database to answer user questions and retrieve information using SQL commands.
  - **Quiz Chatbot:** A chatbot that quizzes users on specific topics, evaluates responses, and provides detailed feedback to aid learning and comprehension.
  
- **CV Extractor:** Extracts information from PDF or Word files, highlighting essential details for viewers. Utilizes Optical Character Recognition (OCR) for unextracted data from PDFs.
- **Website Summarizer:** A tool designed to scrape data from blogs or websites and summarize their content, providing users with a concise overview of the site's topic.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gpt-experiments.git
   ```

2. Navigate to the project directory:
   ```bash
   cd gpt-experiments
   ```

3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables (if necessary) for your OpenAI API key and database configurations.
