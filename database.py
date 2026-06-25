import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            source TEXT,
            published_at TIMESTAMP,
            url TEXT UNIQUE,
            sentiment TEXT,
            confidence FLOAT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Table ready.")

if __name__ == "__main__":
    create_table()