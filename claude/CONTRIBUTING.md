# Contributing & Development Notes

This file documents the development conventions for this project — how to work on it, what the coding standards are, and what to do before committing.

---

## Branching

| Branch | Purpose |
|--------|---------|
| `master` | Stable, working code only |
| `dev` | Active development |

Always develop on `dev` and merge into `master` only when a stage is complete and tested.

To create and switch to a dev branch:
```bash
git checkout -b dev
```

---

## Before Every Commit

1. Make sure `(venv)` is active
2. Test that your script actually runs without errors
3. Never commit `.env` — check `.gitignore` is working
4. Write a clear commit message describing *what changed and why*

### Good commit messages
```
add fetcher.py - pulls headlines from NewsAPI
fix: handle missing articles key in API response
add database.py - store headlines in PostgreSQL
```

### Bad commit messages
```
update
fix stuff
wip
```

---

## Environment Variables

All secrets go in `.env` — never hardcoded in scripts.

| Variable | Description |
|----------|-------------|
| `NEWSAPI_KEY` | Your NewsAPI key from newsapi.org |
| `DB_URL` | PostgreSQL connection string (added in Stage 3) |

---

## Installing New Dependencies

When you install a new library, update `requirements.txt`:
```bash
pip install some-library
pip freeze > requirements.txt
```

This ensures anyone cloning the repo can recreate your exact environment.
