import requests
from bs4 import BeautifulSoup
import openai


def fetch_and_clean_text(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to fetch website content."

        soup = BeautifulSoup(response.content, "html.parser")
        extracted_text = [
            tag.get_text(strip=True)
            for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "li"])
            if tag.get_text(strip=True)
        ]
        cleaned_text = " ".join(extracted_text)
        return cleaned_text
    except Exception as e:
        return f"Error fetching or parsing website content: {str(e)}"


def create_completion(client, cleaned_text, delimiter="####"):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"{delimiter} Summarize what the extracted website text is talking about:\n ",
                },
                {"role": "user", "content": cleaned_text},
            ],
        )
        return response, None
    except Exception as e:
        return None, str(e)


def handle_web_scraping(url):
    cleaned_text = fetch_and_clean_text(url)
    print(cleaned_text)
    if "Error" in cleaned_text:
        return {"error": cleaned_text}, 400
    elif cleaned_text == "Failed to fetch website content.":
        return {"error": "Failed to fetch website content"}, 400
    print("HHHHHHHHHHHH")
    client = openai.OpenAI()
    response, error = create_completion(client, cleaned_text, delimiter="####")
    print("222222")

    if error:
        return {"error": f"LLM processing error: {error}"}, 500

    if response is None:
        return {"error": "Failed to process the text with the LLM"}, 500

    extracted_data = {"answer": response.choices[0].message.content}
    return extracted_data, 200
