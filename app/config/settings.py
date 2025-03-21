import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "gemini": os.getenv("GEMINI_API_KEY"),
    "groq": os.getenv("GROQ_API_KEY"),
    "fireworks": os.getenv("FIREWORKS_API_KEY"),
}

for key, value in API_KEYS.items():
    if not value:
        raise ValueError(f"⚠️ {key.upper()}_API_KEY is missing. Please set it in the .env file.")
