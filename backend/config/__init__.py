import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def sanitize_env_variable(var):
    """Sanitize environment variables by stripping quotes."""
    return var.strip('"').strip("'") if var else var

# Application configurations
SECRET_KEY = sanitize_env_variable(os.getenv("SECRET_KEY"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{sanitize_env_variable(os.getenv('DB_USER'))}:"
    f"{sanitize_env_variable(os.getenv('DB_PASSWORD'))}"
    f"@{sanitize_env_variable(os.getenv('DB_HOST'))}:"
    f"{sanitize_env_variable(os.getenv('DB_PORT'))}/"
    f"{sanitize_env_variable(os.getenv('DB_NAME'))}"
)

# Debugging output for environment variables
print("Database Configuration Debugging:")
print("DB_PORT:", os.getenv('DB_PORT'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_HOST:", os.getenv('DB_HOST'))

print("SQLALCHEMY_DATABASE_URI:", SQLALCHEMY_DATABASE_URI)
