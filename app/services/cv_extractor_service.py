import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from openai import OpenAI
import pdfplumber
import docx
from pdf2image import convert_from_path
import pytesseract

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

client = OpenAI()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    try:
                        images = convert_from_path(
                            file_path,
                            first_page=page.page_number,
                            last_page=page.page_number,
                        )
                        for img in images:
                            text += pytesseract.image_to_string(img) + "\n"
                    except Exception as e:
                        print(f"Error converting page {page.page_number} to image: {e}")
    except Exception as e:
        print(f"Error opening PDF file: {e}")

    return text.strip()


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def create_completion(client, extracted_data, delimiter="####"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"{delimiter} Your task is to extract the following details from the (CV extracted text):\n"
                    "Personal Information:\n"
                    "• Name\n"
                    "• Gender\n"
                    "• Age\n"
                    "Education:\n"
                    "• Academic level (e.g., Bachelor Degree)\n"
                    "• Institution (e.g., University of Dubai)\n"
                    "• GPA/Grade (e.g., 3.9 GPA)\n"
                    "• Start date – End date\n"
                    "Work Experience:\n"
                    "• Company\n"
                    "• Location\n"
                    "• Role\n"
                    "• Start date – End date\n"
                    "• Description\n"
                    f"{delimiter} Please use the same structure to view the result.\n"
                    f"{delimiter} A CV might have multiple entries for education or work experience.\n"
                    f"{delimiter} Don't add anything to the response, start from Personal Information to the Description of the work experience in structured format.\n",
                },
                {"role": "user", "content": extracted_data["text"]},
            ],
        )
        return response
    except Exception as e:
        print(f"Error creating completion: {e}")
        return None


def upload_cv():
    if "cv" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["cv"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        extracted_data = {}
        if filename.endswith(".pdf"):
            extracted_data["text"] = extract_text_from_pdf(file_path)
        elif filename.endswith(".docx") or filename.endswith(".doc"):
            extracted_data["text"] = extract_text_from_docx(file_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if not extracted_data["text"]:
            return jsonify({"error": "No text extracted from the document"}), 400

        response = create_completion(client, extracted_data, delimiter="####")

        if response is None:
            return jsonify({"error": "Failed to process the text with the LLM"}), 500

        extracted_data["answer"] = response.choices[0].message.content
        return jsonify(extracted_data), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400
