import pymupdf4llm
import requests
import tempfile


def convert_pdf_to_markdown(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf_path = temp_pdf.name

        md_text = pymupdf4llm.to_markdown(temp_pdf_path)

        return {"status": "success", "response": md_text}, 200
    except Exception as e:
        return {"status": "error", "response": str(e)}, 500
