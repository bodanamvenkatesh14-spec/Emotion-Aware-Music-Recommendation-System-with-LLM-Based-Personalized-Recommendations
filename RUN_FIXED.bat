@echo off
echo ===================================================
echo 🛠️ FIXING ENVIRONMENT AND STARTING APP
echo ===================================================
echo.

echo Step 1: Creating a Python 3.11 virtual environment using uv...
uv venv --python 3.11
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create venv. Make sure 'uv' is installed and in your PATH.
    pause
    exit /b %errorlevel%
)

echo.
echo Step 2: Activating the environment...
call .venv\Scripts\activate

echo.
echo Step 3: Installing dependencies (this will be super fast with uv)...
uv pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b %errorlevel%
)

echo.
echo ===================================================
echo ✅ ENVIRONMENT FIXED. STARTING APP NOW!
echo ===================================================
echo.

python app.py
pause
