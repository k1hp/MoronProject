import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_CONNECTION = os.getenv("DATABASE_CONNECTION")
PASSWORD_SECRET = os.getenv("PASSWORD_SECRET")


BASE_DIR = Path(__file__).parent.parent
YAMLS_DIR = BASE_DIR / "flask_app/yaml_files/"
