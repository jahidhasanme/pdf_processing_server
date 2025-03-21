import PyPDF2
import requests
import io


def convert_pdf_to_text(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        return {"status": "success", "response": text}, 200
    except Exception as e:
        return {"status": "error", "response": str(e)}, 500
