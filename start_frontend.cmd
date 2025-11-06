@echo off
cd /d "%~dp0\frontend"
if not exist node_modules (
  echo Installing frontend dependencies...
  npm install
)
REM Start Vite on 127.0.0.1:5173
npm run dev -- --host 127.0.0.1 --port 5173

