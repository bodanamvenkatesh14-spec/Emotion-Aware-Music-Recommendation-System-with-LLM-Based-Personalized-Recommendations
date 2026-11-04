@echo off
REM ========================================
REM Emotion Music AI - Quick Start
REM ========================================
REM Double-click this file to start the app!
REM ========================================

echo.
echo ========================================
echo   Emotion Music AI - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    echo.
    echo Dependencies installed!
)

REM Start the application
echo.
echo ========================================
echo   Starting Server...
echo ========================================
echo.
echo Server will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
