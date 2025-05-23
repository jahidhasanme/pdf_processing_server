import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from app.services.file_upload import upload_file_to_s3
from app.services.extract_relevant_text import extract_relevant_text
from app.services.ghibli_service import generate_ghibli_image

response_bp = Blueprint("response", __name__)

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
            data["prompt"], data["path_of_files"], top_n
        )
        return jsonify({"success": True, "data": {"response": response}}), 200
    except Exception as e:
        return jsonify({"status": "error", "response": str(e)}), 500



@response_bp.route("/api/v1/ghibli-style-maker", methods=["POST"])
def ghibli_style_maker():
    data = request.json

    if not data or "prompt" not in data or "image_url" not in data:
        return (
            jsonify(
                {"status": "error", "response": "Prompt and image_url are required"}
            ),
            400,
        )

    try:
        response = generate_ghibli_image(data["prompt"], data["image_url"])
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
