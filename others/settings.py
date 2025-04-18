import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def create_connection(
    user: str, password: str, port: str = "3306", host: str = "mysql_db"
) -> str:
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/"


DB_CONNECTION = create_connection(
    user=os.getenv("MYSQL_USERNAME"),
    password=os.getenv("MYSQL_PWD"),
    port=os.getenv("DATABASE_PORT"),
)
print(DB_CONNECTION)
DB_NAME = os.getenv("DATABASE_NAME")
PASSWORD_SECRET = os.getenv("PASSWORD_SECRET")


BASE_DIR = Path(__file__).parent.parent
YAMLS_DIR = BASE_DIR / "flask_app/yaml_files/"
