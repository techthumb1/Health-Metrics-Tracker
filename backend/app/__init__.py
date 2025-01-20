from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
import logging

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    try:
        app.config.from_object("backend.config")
        logger.info(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    except Exception as e:
        logger.error(f"Configuration error: {str(e)}")
        raise e

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Enable CORS for all routes

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import models within app context to avoid circular imports
    with app.app_context():
        from .models import User  # Import models here
        
        try:
            db.create_all()  # Ensure all tables are created
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise e

    # Set up the user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    try:
        from .views import main
        app.register_blueprint(main)
        logger.info("Blueprints registered successfully")
    except Exception as e:
        logger.error(f"Blueprint registration error: {str(e)}")
        raise e

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error"}, 500

    return app