from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.response_routes import response_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/api/*": {
        "origins": [
            "https://codex4learner.com", 
            "https://openai4pdf.vercel.app", 
            "http://localhost:3000", 
            "http://127.0.0.1:3000",
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True 
    }})

    app.register_blueprint(response_bp)
    return app
