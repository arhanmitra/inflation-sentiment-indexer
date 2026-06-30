# Inflation Sentiment Indexer

A real-time NLP pipeline that tracks consumer sentiment around inflation and cost of living using news headlines. Built with Python, FinBERT, PostgreSQL, and Streamlit.

---

## What It Does

1. **Fetches** live news headlines about inflation, prices, and cost of living via NewsAPI
2. **Stores** them in a PostgreSQL database
3. **Scores** each headline using FinBERT (a financial sentiment NLP model)
4. **Visualises** a rolling sentiment index on a Streamlit dashboard alongside official CSO inflation figures

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.13 | Core language |
| NewsAPI | News headline data source |
| PostgreSQL | Database storage |
| FinBERT | NLP sentiment model |
| Streamlit | Dashboard / visualisation |
| python-dotenv | Secure API key management |
| requests | HTTP requests to APIs |

---

## Project Structure

```
sentiment-indexer/
├── fetcher.py          # Pulls headlines from NewsAPI
├── database.py         # PostgreSQL connection and storage
├── sentiment.py        # FinBERT sentiment scoring pipeline
├── dashboard.py        # Streamlit visualisation app
├── requirements.txt    # All project dependencies
├── .env                # API keys (never committed to Git)
├── .gitignore          # Files excluded from Git tracking
└── README.md           # This file
```

---

## Setup

### 1. Clone the repo
```bash
git clone http://192.168.0.20:4500/arhan/sentiment-indexer.git
cd sentiment-indexer
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the root folder:
```
NEWSAPI_KEY=your_key_here
```

### 5. Run the fetcher
```bash
python fetcher.py
```

---

## Changelog

All notable changes to this project are documented here in reverse chronological order.

---

### [0.4.0] — 2026-06-29

#### Added
- `dashboard.py` — Streamlit app with rolling sentiment index chart, sentiment breakdown pie chart, and raw headlines table
- `run_pipeline.bat` — runs `fetcher.py` then `sentiment.py` in sequence, appending output to `claude/pipeline_log.txt`
- Windows Task Scheduler job configured to run `run_pipeline.bat` daily at 9am

#### Fixed
- `sentiment.py` crashed with `UnicodeEncodeError` on non-Latin headline characters (e.g. `Ş`) — fixed by adding `sys.stdout.reconfigure(encoding="utf-8")` and wrapping the scoring loop in `try/finally` to guarantee `conn.commit()` even on failure
- `os.getenv('DB_PASSWORD')` returned `None` when scripts were run from a directory other than the project root — fixed by passing `Path(__file__).parent / ".env"` to `load_dotenv()` in `database.py` and `fetcher.py`

#### Changed
- Migrated primary remote to GitHub; Gitea remains as a backup remote
- Squashed git history before pushing to GitHub

---

### [0.3.5] — 2026-06-17

#### Added
- `sentiment.py` — loads FinBERT via `transformers`, fetches unscored headlines from DB, writes sentiment label and confidence score back to each row

#### Changed
- `fetcher.py` updated to call `save_headlines()` and persist filtered articles to PostgreSQL via `ON CONFLICT (url) DO NOTHING`

---

### [0.3.0] — 2026-06-15

#### Added
- `database.py` — psycopg2 connection helper and `create_table()` for the `headlines` table

---

### [0.2.1] — 2026-06-06

#### Added
- Error handling to fetcher.py (timeout, connection errors, bad API key, HTTP errors)

---

### [0.2.0] — 2026-06-06

#### Added
- `fetcher.py` — fetches and filters live inflation headlines from NewsAPI
- Client-side keyword filtering to ensure headline relevance

---

### [0.1.0] — 2026-06-06

#### Added
- Project folder initialised with virtual environment
- `.gitignore` configured to exclude `venv/`, `__pycache__/`, and `.env`
- Git repository initialised and connected to Gitea remote
- `fetcher.py` created — pulls live headlines from NewsAPI using keyword search
- `requests` and `python-dotenv` installed
- `.env` file created locally to store NewsAPI key securely
- `README.md` created with project overview, setup instructions, and changelog

---


