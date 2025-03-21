from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.response_routes import response_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app)
    
    app.register_blueprint(response_bp)
    return app
