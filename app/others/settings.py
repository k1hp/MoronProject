import os

import bcrypt
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


# def create_connection(
#     user: str, password: str, port: str = "5432", host: str = "postgres_db"
# ) -> str:
#     return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/"
def create_connection(
    user: str, password: str, port: str = "5432", host: str = "localhost"
) -> str:
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/"


def get_password_secret():
    result = os.getenv("PASSWORD_SECRET")
    print(result)
    if result is None:
        print("Пароля нет в .env")
        result = bcrypt.gensalt().decode().split("$")[-1]
        with open(BASE_DIR.__str__() + "/.env", "a") as env_file:
            env_file.write(f'\nPASSWORD_SECRET="{result}"')
    result = "$2b$12$" + result
    return result


BASE_DIR = Path(__file__).parent.parent.parent
YAMLS_DIR = BASE_DIR / "app/yaml_files/"

DB_CONNECTION = create_connection(
    user=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PWD"),
)
DB_NAME = os.getenv("DATABASE_NAME")
PASSWORD_SECRET = get_password_secret()

print(DB_CONNECTION)

if __name__ == "__main__":
    print(PASSWORD_SECRET)
    print(BASE_DIR)
    print(BASE_DIR.__str__() + "/.env")
