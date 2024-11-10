# config.py
import os

SECRET_KEY = os.getenv("SECRET_KEY")  # Loaded from .env
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Database Configurations
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
