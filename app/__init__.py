import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import main

db = SQLAlchemy()  # Ensure this is defined at the top level

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)  # Initialize db with the Flask app

    app.register_blueprint(main)
    return app
