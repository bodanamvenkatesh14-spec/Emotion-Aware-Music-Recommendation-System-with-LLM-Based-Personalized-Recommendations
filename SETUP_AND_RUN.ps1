# ========================================
# Emotion Music AI - Windows Setup Script
# ========================================
# This script will:
# 1. Create virtual environment
# 2. Install all dependencies
# 3. Start the application
# ========================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Emotion Music AI - Setup & Start" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit
}

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created!" -ForegroundColor Green
} else {
    Write-Host "`n✓ Virtual environment already exists!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated!" -ForegroundColor Green
} catch {
    Write-Host "⚠ PowerShell execution policy issue detected!" -ForegroundColor Yellow
    Write-Host "Fixing permissions..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Fixed and activated!" -ForegroundColor Green
}

# Check if dependencies are installed
Write-Host "`nChecking dependencies..." -ForegroundColor Yellow
$pipList = pip list
if ($pipList -match "Flask") {
    Write-Host "✓ Dependencies already installed!" -ForegroundColor Green
} else {
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
}

# Start the application
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Starting Emotion Music AI Server..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Server will start on: http://localhost:5000" -ForegroundColor Green
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow
Write-Host "----------------------------------------`n" -ForegroundColor Cyan

# Run the Flask application
python app.py
