from flask import Flask
from flask_uuid import FlaskUUID

from config import Config
from models import db
from routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    flask_uuid = FlaskUUID()
    flask_uuid.init_app(app)
    init_routes(app)

    return app