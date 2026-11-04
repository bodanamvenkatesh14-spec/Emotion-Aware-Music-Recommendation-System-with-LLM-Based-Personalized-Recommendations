# 🎵 Quick Reference Guide

## Instant Start

```powershell
cd C:\Users\91765\.gemini\antigravity\scratch\emotion-music-ai
.\start.ps1
```

Then open: **http://localhost:5000**

## Project Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Flask backend server |
| `start.ps1` | Automated setup & start script |
| `requirements.txt` | Python dependencies |
| `.env` | Configuration (Spotify API keys) |
| `README.md` | Project overview |
| `SETUP.md` | Detailed installation guide |
| `DOCUMENTATION.md` | Technical documentation |
| `PROJECT_SUMMARY.md` | Complete feature summary |

### Models
- `models/emotion_detector.py` - CNN for facial emotion detection
- `models/text_analyzer.py` - NLP sentiment analysis
- `models/music_recommender.py` - Spotify music recommendations

### Frontend
- `static/css/style.css` - Premium glassmorphism design
- `static/js/app.js` - Interactive UI logic
- `templates/index.html` - Main application page

## Common Commands

### First Time Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install dependencies  
pip install -r requirements.txt

# Run the app
python app.py
```

### Subsequent Runs
```powershell
# Activate venv
.\venv\Scripts\activate

# Run the app
python app.py
```

Or simply:
```powershell
.\start.ps1
```

## Spotify Setup (Optional)

1. Go to https://developer.spotify.com/dashboard
2. Create an app
3. Copy Client ID and Client Secret
4. Edit `.env` file and paste your credentials

Without Spotify: App uses curated fallback playlists (still works great!)

## How to Use

1. **Camera Mode**: Show your face → Click "Capture & Analyze"
2. **Text Mode**: Describe your mood → Click "Analyze Text"  
3. **Both Mode**: Use camera + text for best results

## Troubleshooting

**Camera not working?**
- Grant camera permissions in browser
- Try Chrome or Edge browser

**Import errors?**
```powershell
pip install -r requirements.txt --force-reinstall
```

**Port 5000 busy?**
Edit `app.py`, change last line to:
```python
app.run(debug=True, port=5001)
```

## Features

✅ Real-time facial emotion detection (CNN)  
✅ Text sentiment analysis (NLP)  
✅ Multi-modal analysis (face + text)  
✅ Spotify music recommendations  
✅ Beautiful glassmorphism UI  
✅ Fully responsive design  
✅ Privacy-first (no data storage)  

## Support

- Read `SETUP.md` for detailed installation
- Check `DOCUMENTATION.md` for technical details
- See `PROJECT_SUMMARY.md` for complete overview

---

**Built with ❤️ using AI & Machine Learning**
