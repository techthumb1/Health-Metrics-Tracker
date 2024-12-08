# run.py
from dotenv import load_dotenv
import os


# Explicitly specify the path to the .env file
load_dotenv(dotenv_path=".env")

# Debugging to ensure variables are loaded
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_PORT:", os.getenv('DB_PORT'))
print("DB_NAME:", os.getenv('DB_NAME'))

from app import create_app, db
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
