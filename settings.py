import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION = os.getenv("DATABASE_CONNECTION")
