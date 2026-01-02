@echo off
echo Setting up AI Resume Analyzer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your OpenAI API key!
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run 'run.bat' to start the application
echo.
pause
