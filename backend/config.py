# config.py
import os

SECRET_KEY = os.getenv("SECRET_KEY") 
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Database Configurations
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

print(os.getenv('DATABASE_URL'))
print("DB_PORT:", os.getenv('DB_PORT'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_NAME:", os.getenv('DB_NAME'))