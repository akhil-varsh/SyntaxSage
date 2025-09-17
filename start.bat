@echo off
title SyntaxSage - AI Code Analysis Tool
echo.
echo ========================================
echo   SyntaxSage - AI Code Analysis Tool
echo ========================================
echo.
echo Checking prerequisites...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if Ollama is running
echo Checking Ollama connection...
curl -s http://localhost:11434/api/version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama might not be running
    echo Please ensure Ollama is installed and running with:
    echo   ollama serve
    echo   ollama pull llama3.1
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

REM Install dependencies if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Start the application
echo.
echo Starting SyntaxSage...
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause