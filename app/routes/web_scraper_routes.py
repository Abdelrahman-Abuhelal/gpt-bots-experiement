from flask import Blueprint, render_template, request, jsonify
from ..services.web_scraper_service import handle_web_scraping

main = Blueprint("web_scraper", __name__)


@main.route("/web-scraper-page")
def web_scraper_page():
    return render_template("web_scraper.html")


@main.route("/web-scraper", methods=["POST"])
def web_scraper_route():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        result, status_code = handle_web_scraping(url)  # Unpack the tuple here
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
