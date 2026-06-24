import os
from typing import Any

import psycopg2
from dotenv import load_dotenv

from .models.user_db import UserRepository

load_dotenv()

conn: Any = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("PASSWORD"),
)


def get_user_repository() -> UserRepository:
    return UserRepository(conn)
