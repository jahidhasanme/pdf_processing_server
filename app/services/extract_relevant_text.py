import pytesseract
from PIL import Image
import fitz
import markdown
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
from rank_bm25 import BM25Okapi
from langdetect import detect
from deep_translator import GoogleTranslator
import requests
import os
import tempfile
import mimetypes


nltk.download("punkt")
nltk.download("punkt_tab")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])


def extract_text_from_md(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read())
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return str(e)


def split_into_sentences(text):
    return sent_tokenize(text)


def translate_query(query, target_lang="en"):
    detected_lang = detect(query)
    if detected_lang != target_lang:
        return GoogleTranslator(source=detected_lang, target=target_lang).translate(
            query
        )
    return query


def search_with_bm25(query, sentences, top_n=5):
    tokenized_sentences = [s.split() for s in sentences]
    bm25 = BM25Okapi(tokenized_sentences)
    query_tokens = query.split()
    scores = bm25.get_scores(query_tokens)
    return [
        sentences[i]
        for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
            :top_n
        ]
    ]


def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None


def get_file_extension_from_mime(mime_type):
    mime_to_ext = {
        "application/pdf": ".pdf",
        "text/markdown": ".md",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/jpg": ".jpg",
    }
    return mime_to_ext.get(mime_type, "")


def extract_relevant_text(prompt, path_of_files, top_n=100, algorithm_name="bm25"):
    sentences = []

    for file_path in path_of_files:
        if file_path.startswith("http"):
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            downloaded_file = download_file(file_path, temp_file.name)
            if downloaded_file:
                mime_type, _ = mimetypes.guess_type(file_path)
                extension = get_file_extension_from_mime(mime_type)
                if extension:
                    new_temp_file = temp_file.name + extension
                    os.rename(temp_file.name, new_temp_file)
                    file_path = new_temp_file
                else:
                    return "Unsupported MIME type"
            else:
                return "Error downloading file."

        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)

        elif file_path.endswith(".md"):
            text = extract_text_from_md(file_path)

        elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
            text = extract_text_from_image(file_path)

        else:
            raise ValueError("Unsupported file format: " + file_path)

        sentences.extend(split_into_sentences(text))

        if file_path.endswith(temp_file.name):
            os.remove(file_path)

    translated_query = translate_query(prompt)

    return "\n".join(search_with_bm25(translated_query, sentences, top_n))
