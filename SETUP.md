# 🎵 Emotion-Aware Music Recommendation System
# Setup and Installation Guide

## Quick Start Guide

### 1. Install Python Dependencies

Open PowerShell in this directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Note**: Installation may take 5-10 minutes as it downloads TensorFlow and other ML libraries.

### 2. Set Up Spotify API (Optional but Recommended)

To get real music recommendations from Spotify:

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account (create one if needed)
3. Click "Create App"
4. Fill in the form:
   - App Name: "Emotion Music Recommender"
   - App Description: "AI-powered mood-based music recommendation"
   - Redirect URI: http://localhost:5000 (just for registration)
   - Check "Web API"
5. Click "Save"
6. Copy your **Client ID** and **Client Secret**

7. In this project directory, create `.env` file:
```powershell
Copy-Item .env.example .env
```

8. Open `.env` and paste your credentials:
```
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_random_secret_key_123
```

**If you skip this step**: The system will use fallback curated playlists (still works great!)

### 3. Run the Application

```powershell
# Make sure virtual environment is activated
python app.py
```

You should see:
```
🎵 Initializing Emotion-Aware Music Recommendation System...
✓ Emotion detection model loaded successfully
✓ Text sentiment analyzer loaded successfully
✓ Spotify API connected successfully (or fallback message)
✓ System ready!

🚀 Starting server...
📍 Open http://localhost:5000 in your browser
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

Grant camera permissions when prompted!

## 🎯 How to Use

### Camera Mode 📷
1. Click "Camera" mode
2. Position your face in view
3. Click "Capture & Analyze"
4. Get music based on your facial expression!

### Text Mode 💬
1. Click "Text" mode
2. Type how you're feeling
3. Click "Analyze Text"
4. Get mood-matching music!

### Combined Mode ✨ (Most Accurate)
1. Click "Both" mode
2. Show your face AND describe your mood
3. Click "Analyze Everything"
4. Get the best possible recommendations!

## 🔧 Troubleshooting

### Camera not working?
- Grant camera permissions in browser
- Make sure no other app is using the camera
- Try a different browser (Chrome/Edge recommended)

### Missing dependencies error?
```powershell
pip install -r requirements.txt --force-reinstall
```

### TensorFlow installation issues?
For Windows with no GPU:
```powershell
pip install tensorflow-cpu
```

### Port 5000 already in use?
Change the port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📊 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Camera**: Any webcam
- **Browser**: Chrome, Edge, Firefox, or Safari
- **Internet**: Required for Spotify API and downloading models

## 🚀 Advanced: Training Your Own Model

The system uses a pre-built architecture. To train on custom data:

1. Prepare dataset (FER2013 recommended)
2. Modify `models/emotion_detector.py`
3. Add training code
4. Train and save model to `static/models/emotion_model.h5`

## 📝 Notes

- First run downloads the sentiment analysis model (~250MB)
- Model files are saved in `static/models/`
- The app works offline (except Spotify features)
- All emotion detection happens locally (privacy-first!)

## 🎓 Educational Value

This project demonstrates:
- ✅ Computer Vision (CNN for facial recognition)
- ✅ Natural Language Processing (Sentiment analysis)
- ✅ Deep Learning (TensorFlow/Keras)
- ✅ API Integration (Spotify)
- ✅ Full-stack Development (Flask + Vanilla JS)
- ✅ Recommender Systems
- ✅ Real-time Processing

Perfect for ML/AI portfolio projects!

## 📞 Support

If you encounter issues:
1. Check console output for error messages
2. Verify all dependencies are installed
3. Check browser console (F12) for JavaScript errors
4. Ensure camera permissions are granted

Enjoy your emotion-aware music experience! 🎵✨
