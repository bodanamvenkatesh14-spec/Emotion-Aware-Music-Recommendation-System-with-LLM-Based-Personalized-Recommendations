# Quick Start Script for Emotion-Aware Music Recommender
# Run this script to set up and start the application

Write-Host "`n🎵 Emotion-Aware Music Recommendation System - Quick Start" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Check Python installation
Write-Host "`n[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
Write-Host "`n[2/5] Setting up virtual environment..." -ForegroundColor Yellow
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[3/5] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`n[4/5] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes on first run..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ Some dependencies may have failed. Check output above." -ForegroundColor Yellow
}

# Check Spotify configuration
Write-Host "`n[5/5] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "your_client_id_here") {
        Write-Host "⚠ Spotify API not configured - app will use fallback playlists" -ForegroundColor Yellow
        Write-Host "  To enable Spotify: Edit .env file with your API credentials" -ForegroundColor Gray
        Write-Host "  Get credentials from: https://developer.spotify.com/dashboard" -ForegroundColor Gray
    } else {
        Write-Host "✓ Spotify API configured" -ForegroundColor Green
    }
} else {
    Write-Host "✓ Using default configuration" -ForegroundColor Green
}

# Start the application
Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🚀 Starting Emotion-Aware Music Recommender..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Run the Flask app
python app.py
