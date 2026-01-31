@echo off
echo ==========================================
echo   Installing YT Music to MP3 Converter
echo ==========================================

:: 1. Setup Backend
echo [1/2] Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

:: 2. Setup Frontend
echo [2/2] Setting up Frontend...
cd frontend
npm install
cd ..

echo ==========================================
echo   Installation Complete! 
echo   Make sure FFmpeg is installed on your PC.
echo   Run 'run_project.bat' to start the app.
echo ==========================================
pause