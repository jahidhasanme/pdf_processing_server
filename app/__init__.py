from flask import Flask
from flask_cors import CORS
from app.routes.response_routes import response_bp

def create_app():
    app = Flask(__name__)
    
    CORS(app, origins="*")
    app.register_blueprint(response_bp)

    return app
