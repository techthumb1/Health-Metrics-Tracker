# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Attach Flask-Migrate to app and db

    login_manager.login_view = 'main.login'

    # Register Blueprints after initializing db to avoid circular imports
    from .views import main
    app.register_blueprint(main)

    # Import models only within the app context to avoid circular import
    with app.app_context():
        from .models import User  # Import models here for user_loader

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
