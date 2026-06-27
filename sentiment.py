from transformers import pipeline
from database import get_connection
from pathlib import Path
from dotenv import load_dotenv
import sys

load_dotenv(Path(__file__).parent / ".env")
sys.stdout.reconfigure(encoding="utf-8")

def load_model():
    print("Loading FinBERT model...")
    return pipeline("text-classification", model="ProsusAI/finbert")

def score_headlines():
    classifier = load_model()
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch only unscored headlines
    cursor.execute("""
        SELECT id, title FROM headlines
        WHERE sentiment IS NULL
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No unscored headlines found.")
        cursor.close()
        conn.close()
        return

    print(f"Scoring {len(rows)} headlines...\n")

    try:
        for row in rows:
            id, title = row
            result = classifier(title)[0]
            sentiment = result["label"]
            confidence = round(result["score"], 4)

            cursor.execute("""
                UPDATE headlines
                SET sentiment = %s, confidence = %s
                WHERE id = %s
            """, (sentiment, confidence, id))

            print(f"{sentiment} ({confidence}) | {title}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

    print(f"\nDone. Scored {len(rows)} headlines.")

score_headlines()