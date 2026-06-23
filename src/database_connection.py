import psycopg2, os
from dotenv import load_dotenv
from .models.user_db import UserRepository

load_dotenv()

conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("PASSWORD"),
        )

def get_user_repository():
    return UserRepository(conn)