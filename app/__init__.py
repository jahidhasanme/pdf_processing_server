from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.response_routes import response_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={
        r"/*": {
            "origins": [
                "https://openai4pdf.vercel.app",
                "http://localhost:3000"
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    app.register_blueprint(response_bp)
    return app
