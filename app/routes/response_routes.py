from flask import Blueprint, request, jsonify
from app.services.convert_large_pdf import convert_large_pdf_to_text
from app.services.convert_pdf_text import convert_pdf_to_text
from app.services.convert_pdf_markdown import convert_pdf_to_markdown

response_bp = Blueprint("response", __name__)


@response_bp.route("/api/convert-large-pdf-to-text", methods=["POST"])
def get_large_pdf_to_text():
    data = request.json
    if not data or "pdfUrl" not in data:
        return jsonify({"status": "error", "response": "PDF URL is required"}), 400

    return convert_large_pdf_to_text(data["pdfUrl"])


@response_bp.route("/api/convert-pdf-to-text", methods=["POST"])
def get_pdf_to_text():
    data = request.json
    if not data or "pdfUrl" not in data:
        return jsonify({"status": "error", "response": "PDF URL is required"}), 400

    return convert_pdf_to_text(data["pdfUrl"])


@response_bp.route("/api/convert-pdf-to-markdown", methods=["POST"])
def get_pdf_to_markdown():
    data = request.json
    if not data or "pdfUrl" not in data:
        return jsonify({"status": "error", "response": "PDF URL is required"}), 400

    return convert_pdf_to_markdown(data["pdfUrl"])
