@echo off
cd C:\dev\sentiment-indexer
call venv\Scripts\activate.bat
python fetcher.py >> claude\pipeline_log.txt 2>&1
python sentiment.py >> claude\pipeline_log.txt 2>&1