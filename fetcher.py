import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import psycopg2
from database import get_connection

load_dotenv(Path(__file__).parent / ".env")
API_KEY = os.getenv("NEWSAPI_KEY")

KEYWORDS = ["inflation", "cost of living", "prices", "rent", "cpi", "interest rate"]

def fetch_headlines():
    if not API_KEY:
        print("Error: NEWSAPI_KEY not found. Check your .env file.")
        return

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "inflation OR \"cost of living\" OR CPI",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print(f"API error: {data.get('message', 'Unknown error')}")
            return

        filtered = [
            article for article in data["articles"]
            if any(kw in article["title"].lower() for kw in KEYWORDS)
        ]

        print(f"Found {len(filtered)} relevant headlines\n")
        save_headlines(filtered)

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Check your internet connection.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to NewsAPI. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")

def save_headlines(articles):
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO headlines (title, source, published_at, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
            """, (
                article["title"],
                article["source"]["name"],
                article["publishedAt"],
                article["url"]
            ))
            saved += 1
        except Exception as e:
            print(f"Skipped article: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {saved} new headlines to database.")

fetch_headlines()