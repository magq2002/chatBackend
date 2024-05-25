from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from .blueprints.messages.routes import messages_bp
from .blueprints.voice_messages.routes import voice_messages_bp
from dotenv import load_dotenv

load_dotenv()

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(voice_messages_bp, url_prefix='/voice_messages')

    return app
