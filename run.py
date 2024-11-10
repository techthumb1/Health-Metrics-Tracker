# run.py
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

from app import create_app, db
app = create_app()

with app.app_context():
    db.create_all()  # Creates tables in PostgreSQL

if __name__ == "__main__":
    app.run(debug=True)
