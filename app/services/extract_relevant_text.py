import pytesseract
from PIL import Image
import fitz
import markdown
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util
from langdetect import detect
from deep_translator import GoogleTranslator
import requests
import os
import tempfile
import mimetypes
import multiprocessing

# Download NLTK data
nltk.download("punkt")

# Sentence transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            return "\n".join([page.get_text("text") for page in doc])
    except Exception as e:
        return str(e)

def extract_text_from_md(md_path):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            html = markdown.markdown(f.read())
            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text()
    except Exception as e:
        return str(e)

def extract_text_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img)
    except Exception as e:
        return str(e)

def split_into_sentences(text):
    return sent_tokenize(text)

def translate_query(query, target_lang="en", cache={}):
    if query in cache:
        return cache[query]
    detected_lang = detect(query)
    if detected_lang != target_lang:
        translated = GoogleTranslator(source=detected_lang, target=target_lang).translate(query)
        cache[query] = translated
        return translated
    return query

def search_with_tfidf(query, sentences, top_n=5):
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(sentences)
    query_vector = vectorizer.transform([query])
    scores = (sentence_vectors * query_vector.T).toarray().flatten()
    return [sentences[i] for i in scores.argsort()[-top_n:][::-1]]

def search_with_bm25(query, sentences, top_n=5):
    tokenized_sentences = [s.split() for s in sentences]
    bm25 = BM25Okapi(tokenized_sentences)
    scores = bm25.get_scores(query.split())
    return [sentences[i] for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]]

def search_with_similarity(query, sentences, top_n=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]
    return [sentences[i] for i in similarities.argsort(descending=True)[:top_n]]

def keyword_search(query, sentences, top_n=5):
    query_words = query.lower().split()
    return [s for s in sentences if any(q in s.lower() for q in query_words)][:top_n] or ["No relevant sentences found."]

def download_file(url):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(temp_file.name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return temp_file.name
    except requests.exceptions.RequestException as e:
        return None

def get_file_extension_from_mime(mime_type):
    mime_to_ext = {'application/pdf': '.pdf', 'text/markdown': '.md', 'image/jpeg': '.jpg', 'image/png': '.png'}
    return mime_to_ext.get(mime_type, '')

def process_file(file_path):
    if file_path.startswith("http"):
        file_path = download_file(file_path)
        if not file_path:
            return None
    
    text = ""
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".md"):
        text = extract_text_from_md(file_path)
    elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(file_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    return split_into_sentences(text)

def extract_relevant_text(prompt, path_of_files, top_n=100, algorithm_name="tf-idf"):
    sentences = []
    
    with multiprocessing.Pool(processes=min(4, len(path_of_files))) as pool:
        results = pool.map(process_file, path_of_files)
    
    for result in results:
        if result:
            sentences.extend(result)

    translated_query = translate_query(prompt)

    if algorithm_name == "tf-idf":
        return "\n".join(search_with_tfidf(translated_query, sentences, top_n))
    elif algorithm_name == "bm25":
        return "\n".join(search_with_bm25(translated_query, sentences, top_n))
    elif algorithm_name == "context-based":
        return "\n".join(search_with_similarity(translated_query, sentences, top_n))
    elif algorithm_name == "keyword":
        return "\n".join(keyword_search(translated_query, sentences, top_n))
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm_name}")
