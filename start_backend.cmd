@echo off
cd /d "%~dp0"
REM Start FastAPI backend on 127.0.0.1:8000
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

