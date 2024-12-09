# GPT Experiments

## Overview

**GPT Experiments** is a Flask-based project showcasing my expertise in LLMs (Large Language Models) and Generative AI. Designed with a focus on practical applications, this project integrates advanced AI-driven solutions for diverse use cases, such as implementations of chatbots using OpenAI's API, alongside a CV extractor for processing document files. It currently features four distinct chatbots, each with unique functionalities, also a tool for extracting information from CVs in PDF or Word formats and tool to summarize any website article.

## Table of Contents

- [Features](#features)
- [Installation](#installation)

## Features

- Four chatbots with different capabilities:
  - **Basic Chatbot:** A simple conversational agent with memory and history tracking for unique sessions.
  - **SQLite Chatbot:** Similar to the basic chatbot, but it stores conversation history in an SQLite database.
  - **Database Query Chatbot:** Connects to a database to answer user questions and retrieve information using SQL commands.
  - **Quiz Chatbot:** A chatbot that quizzes users on specific topics, evaluates responses, and provides detailed feedback to aid learning and comprehension.
  
- **CV Extractor:** Extracts information from PDF or Word files, highlighting essential details for viewers. Utilizes Optical Character Recognition (OCR) for unextracted data from PDFs.
- **Website Summarizer:** A tool designed to scrape data from blogs or websites and summarize their content, providing users with a concise overview of the site's topic.

![image](https://github.com/user-attachments/assets/72b73f28-d169-4ec8-99fb-129bb5daf3ad)

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
