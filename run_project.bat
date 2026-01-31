@echo off
echo ==========================================
echo   Starting YT Music to MP3 Converter...
echo ==========================================

:: Start Backend in a new window
start cmd /k "echo Starting Backend... && cd backend && venv\Scripts\activate && python main.py"

:: Start Frontend in a new window
start cmd /k "echo Starting Frontend... && cd frontend && npm start"

echo ==========================================
echo   Services are starting!
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo ==========================================