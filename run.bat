@echo off
echo Starting AI Resume Analyzer...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please run setup.bat first and configure your API key.
    pause
    exit /b 1
)

REM Start the application
echo Server starting at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
