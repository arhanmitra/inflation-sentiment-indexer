# Architecture Overview

This document explains how the different parts of the project fit together.

---

## Data Flow

```
NewsAPI
   │
   │  HTTP request (fetcher.py)
   ▼
Raw JSON headlines
   │
   │  Parse & clean
   ▼
PostgreSQL Database
   │
   │  Read unscored headlines (sentiment.py)
   ▼
FinBERT NLP Model
   │
   │  Returns score: positive / negative / neutral
   ▼
PostgreSQL Database (scores stored)
   │
   │  Query scored headlines (dashboard.py)
   ▼
Streamlit Dashboard
```

---

## Files & Responsibilities

### `fetcher.py`
- Connects to NewsAPI
- Searches for keywords: "inflation", "cost of living", "prices"
- Parses JSON response
- Stores raw headlines in PostgreSQL

### `database.py`
- Manages the PostgreSQL connection
- Creates tables if they don't exist
- Handles insert and query operations
- Keeps all DB logic in one place (not scattered across scripts)

### `sentiment.py`
- Loads FinBERT model
- Reads unscored headlines from the database
- Scores each one (positive / negative / neutral + confidence score)
- Writes scores back to the database

### `dashboard.py`
- Reads scored headlines from the database
- Calculates a rolling daily sentiment index
- Plots it against official CSO inflation figures
- Runs as a local Streamlit web app

---

## Database Schema (planned)

### Table: `headlines`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PRIMARY KEY | Auto-incrementing ID |
| `title` | TEXT | Headline text |
| `source` | TEXT | News source name |
| `published_at` | TIMESTAMP | Publication date |
| `url` | TEXT | Article URL |
| `sentiment` | TEXT | positive / negative / neutral |
| `confidence` | FLOAT | Model confidence score 0-1 |
| `created_at` | TIMESTAMP | When we fetched it |
