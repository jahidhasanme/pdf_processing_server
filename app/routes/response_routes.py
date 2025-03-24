import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from app.services.file_upload import upload_file_to_s3
from app.services.convert_large_pdf import convert_large_pdf_to_text
from app.services.convert_pdf_text import convert_pdf_to_text
from app.services.convert_pdf_markdown import convert_pdf_to_markdown
from app.services.extract_relevant_text import extract_relevant_text

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


@response_bp.route("/api/v1/extract-relevant-text", methods=["POST"])
def get_extracted_relevant_text():
    data = request.json

    if not data or "prompt" not in data or "path_of_files" not in data:
        return (
            jsonify(
                {"status": "error", "response": "Prompt and path_of_files are required"}
            ),
            400,
        )

    top_n = data.get("top_n", 100)

    algorithm_name = data.get("algorithm_name", "bm25")

    if not isinstance(data["path_of_files"], list) or len(data["path_of_files"]) == 0:
        return (
            jsonify(
                {
                    "status": "error",
                    "response": "path_of_files must be a non-empty list",
                }
            ),
            400,
        )

    try:
        response = extract_relevant_text(
            data["prompt"], data["path_of_files"], top_n, algorithm_name
        )
        return jsonify({"success": True, "data": {"response": response}}), 200
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500


ALLOWED_EXTENSIONS = {"pdf", ".md", "jpg", "jpeg", "png"}
MAX_FILE_SIZE = 32 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@response_bp.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"status": "error", "response": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "response": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_url = upload_file_to_s3(file, filename)

            response_data = [
                {
                    "url": file_url,
                    "name": filename,
                    "contentType": file.content_type,
                }
            ]

            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({"status": "error", "response": str(e)}), 500

    return (
        jsonify({"status": "error", "response": "Invalid file type or file too large"}),
        400,
    )
