from dotenv import load_dotenv
from backend.app import create_app, db
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = create_app()

# Set up the database within the application context
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Debug environment variables
print("Environment Variables Debug:")
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))

# Run the Flask application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "True").lower() in ["true", "1", "yes"]
    )
