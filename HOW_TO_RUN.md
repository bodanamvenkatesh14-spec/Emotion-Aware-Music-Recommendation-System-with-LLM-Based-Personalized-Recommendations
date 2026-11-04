# 🚀 HOW TO RUN ON ANOTHER COMPUTER

## ✅ **SUPER EASY METHOD** (Recommended)

### **Step 1: Extract the ZIP**
- Extract `emotion-music-ai-CLEAN.zip` to any folder
- Example: `C:\MyProjects\emotion-music-ai\`

### **Step 2: Double-Click to Run**
Simply **double-click** one of these files:

**Option A: `START.bat`** ⭐ (Easiest!)
- Just double-click `START.bat`
- Everything will be set up automatically
- Server will start
- Open browser to `http://localhost:5000`

**Option B: `SETUP_AND_RUN.ps1`**
- Right-click → "Run with PowerShell"
- Colored output with progress
- Server will start automatically

---

## 📋 **MANUAL METHOD** (If you prefer)

### **Step 1: Extract ZIP**
Extract the zip file to any location

### **Step 2: Open Terminal**
- Navigate to the extracted folder
- Right-click → "Open in Terminal" or "Open PowerShell here"

### **Step 3: Set Up Environment**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get an error about execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

### **Step 4: Run the App**
```powershell
python app.py
```

### **Step 5: Open Browser**
Go to: `http://localhost:5000`

---

## ⚡ **QUICK REFERENCE**

### **First Time Setup (Do Once)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **Every Time You Run (After Setup)**
```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

Or just **double-click `START.bat`**! 🎉

---

## 🎯 **What Each File Does**

| File | Purpose | How to Use |
|------|---------|------------|
| `START.bat` | Quick start (easiest!) | Double-click it |
| `SETUP_AND_RUN.ps1` | PowerShell setup | Right-click → Run with PowerShell |
| `app.py` | Main application | `python app.py` |
| `requirements.txt` | Dependencies list | Used during setup |

---

## 📦 **Required Software**

Before running, make sure you have:

✅ **Python 3.8 or higher**
- Download: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

✅ **Web Browser**
- Chrome (recommended)
- Firefox, Edge, or Safari also work

---

## 🎮 **After Starting**

When the server starts, you'll see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

Then:
1. Open your browser
2. Go to: `http://localhost:5000`
3. Use the app!

---

## ⚠️ **Troubleshooting**

### **"Python not found"**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installing

### **"pip not found"**
```powershell
python -m ensurepip --upgrade
```

### **PowerShell script won't run**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Port 5000 already in use**
Edit `app.py` and change the last line:
```python
app.run(debug=True, port=5001)  # Use different port
```

### **Dependencies installation fails**
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

### **TensorFlow won't install (Python 3.13)**
- Python 3.13 has compatibility issues with TensorFlow
- Use Python 3.11 or 3.10 instead
- Download from: https://www.python.org/downloads/

---

## 🎵 **Using The App**

Once running:

### **Camera Mode** 📷
1. Click "Camera Mode"
2. Allow camera access
3. Click "Capture & Analyze"
4. Get Telugu music for your mood!

### **Text Mode** ✍️
1. Click "Text Mode"
2. Type your feelings
3. Click "Analyze Emotion"
4. Get song recommendations!

### **Music Player** 🎵
1. Click ▶️ on any song
2. Player appears at bottom
3. Song opens on YouTube
4. Use Next/Previous buttons
5. Adjust volume

---

## 💡 **Pro Tips**

1. **First Time?** Use `START.bat` - it's the easiest!
2. **Good Lighting** helps camera mode work better
3. **Chrome Browser** works best
4. **Don't close terminal** while using the app
5. **Press Ctrl+C** in terminal to stop server

---

## 🔄 **Updating the App**

To update code or add songs:
1. Stop the server (Ctrl+C)
2. Edit files (e.g., add Telugu songs in `music_recommender.py`)
3. Restart server (run `START.bat` again)
4. Refresh browser

---

## 📁 **Folder Structure**

After extraction, you should see:
```
emotion-music-ai/
├── START.bat              ← Double-click this!
├── SETUP_AND_RUN.ps1     ← Or this!
├── app.py                ← Main app
├── requirements.txt      ← Dependencies
├── models/               ← AI models
├── static/               ← CSS, JavaScript
├── templates/            ← HTML files
└── data/                 ← Face detection data
```

---

## 🎊 **Summary**

**Easiest Way:**
1. Extract ZIP
2. Double-click `START.bat`
3. Open `http://localhost:5000`
4. Enjoy! 🎉

**That's it!**

---

## 📞 **Need Help?**

Check these files:
- `README.md` - Main documentation
- `QUICK_START.md` - Quick reference
- `PROJECT_README.md` - Complete guide
- `MUSIC_PLAYER_GUIDE.md` - Music player help

---

## ✅ **Checklist**

Before running, make sure:
- [ ] Python 3.8+ installed
- [ ] ZIP file extracted
- [ ] In the extracted folder
- [ ] Double-clicked `START.bat`
- [ ] Browser open to `localhost:5000`

**All checked? You're good to go!** 🚀

---

**Made with ❤️ for Telugu music lovers!**
**Enjoy your Emotion-Aware Music Recommendation System!** 🎵
