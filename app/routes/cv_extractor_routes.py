# cv_extractor_routes
from flask import Blueprint, request, jsonify, render_template
from ..services.cv_extractor_service import upload_cv

main = Blueprint("cv_extractor", __name__)


@main.route("/cv-extractor-page")
def cv_extractor_page():
    return render_template("./CVExtractor.html")


@main.route("/cv-extractor", methods=["POST"])
def cv_upload():
    return upload_cv()
