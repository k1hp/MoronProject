import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def create_connection(
    user: str, password: str, port: str = "3306", host: str = "postgres_db"
) -> str:
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/"


DB_CONNECTION = create_connection(
    user=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PWD"),
    port=os.getenv("DATABASE_PORT"),
)
print(DB_CONNECTION)
DB_NAME = os.getenv("DATABASE_NAME")
PASSWORD_SECRET = "$2b$12$" + os.getenv("PASSWORD_SECRET")
print(PASSWORD_SECRET)


BASE_DIR = Path(__file__).parent.parent
YAMLS_DIR = BASE_DIR / "flask_app/yaml_files/"
