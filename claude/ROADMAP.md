# Project Roadmap

This document tracks what's been built, what's in progress, and what's coming next.

---

## Stage 1 — Environment Setup ✅
- [x] Project folder created
- [x] Virtual environment configured
- [x] Git initialised and connected to Gitea
- [x] `.gitignore` set up
- [x] Steering files created (README, ROADMAP, CONTRIBUTING, ARCHITECTURE)

## Stage 2 — Data Ingestion ✅
- [x] NewsAPI account created
- [x] API key stored securely in `.env`
- [x] `requests` and `python-dotenv` installed
- [x] `fetcher.py` tested and returning live headlines
- [X] Error handling added (API failures, missing keys)
- [x] Headlines saved to a local CSV~~ — skipped, going straight to PostgreSQL in Stage 3

## Stage 3 — Database & NLP Pipeline ✅
- [x] PostgreSQL installed and running locally
- [x] `database.py` created — connects Python to PostgreSQL
- [x] Headlines table created in database
- [x] `fetcher.py` updated to store headlines in DB instead of printing
- [x] FinBERT model installed via `transformers`
- [x] `sentiment.py` created — scores each headline
- [x] Sentiment scores stored alongside headlines in DB

## Stage 4 — Dashboard 🔄 In Progress
- [x] `dashboard.py` created with Streamlit
- [x] Rolling sentiment index chart built
- [ ] CSO inflation data imported and overlaid
- [ ] Dashboard deployable locally
- [ ] README updated with demo screenshot
