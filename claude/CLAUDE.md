# sentiment-indexer

A pipeline that fetches inflation-related headlines from NewsAPI, filters them by keyword, and stores them in a PostgreSQL database for sentiment analysis.

## Project structure

- `fetcher.py` — pulls headlines from NewsAPI, filters by keyword, saves to DB
- `database.py` — PostgreSQL connection and table setup
- `.env` — local secrets (not committed)

## Setup

1. Copy `.env` and fill in credentials (see variables below)
2. Run `python database.py` to create the `headlines` table
3. Run `python fetcher.py` to fetch and store headlines

### Required `.env` variables

```
NEWSAPI_KEY=
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

## Changelog

### 2026-06-17

- Added `sentiment.py` — loads FinBERT, fetches unscored headlines from DB, writes sentiment label and confidence back to each row
- Added `dashboard.py` — Streamlit app with rolling sentiment index chart, pie chart breakdown, and raw headlines table

### 2026-06-15

- Added `database.py` with `get_connection()` (psycopg2) and `create_table()` for the `headlines` table
- Updated `fetcher.py` to persist filtered articles via `save_headlines()`, using `ON CONFLICT (url) DO NOTHING` to avoid duplicates
- Fixed `load_dotenv()` in both `database.py` and `fetcher.py` to use `Path(__file__).parent / ".env"` — previously `os.getenv('DB_PASSWORD')` returned `None` when scripts were run from a different working directory
