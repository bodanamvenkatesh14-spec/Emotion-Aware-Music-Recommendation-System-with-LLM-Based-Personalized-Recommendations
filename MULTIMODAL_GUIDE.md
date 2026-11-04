# 🎵 MoodTune AI - Multi-Modal Emotion Music System

## 🌟 Enhanced Features

This enhanced version includes **multi-modal emotion detection** combining multiple inputs for superior accuracy and an **automatic playlist** feature for seamless music playback.

---

## 🎯 New Features

### 1. **Multi-Modal Emotion Detection** 

Combine multiple inputs for the most accurate emotion detection:

#### 👁️ **Facial Expression Analysis**
- Real-time face detection using OpenCV Haar Cascades
- Deep learning CNN model for emotion classification
- Detects: Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral

#### 🎙️ **Voice Tone Analysis**
- Audio feature extraction using Librosa
- Analyzes pitch, energy, tempo, MFCCs, spectral features
- Rule-based emotion classification from voice characteristics
- Records and analyzes voice in real-time

#### 💬 **Text Sentiment Analysis**
- NLP-based sentiment analysis using Transformers
- Analyzes written text for emotional content
- Supports natural language input

#### ❤️ **Heart Rate Monitoring**
- Accepts heart rate data from wearables or manual input
- Analyzes HRV (Heart Rate Variability)
- Maps physiological data to emotional states
- Provides wellness recommendations

### 2. **Intelligent Emotion Fusion**

The system uses a **weighted fusion algorithm** that:
- Combines all available modalities intelligently
- Weights each input by reliability and confidence
- Checks emotion consistency across modalities
- Provides breakdown of each modality's contribution

### 3. **Automatic Music Playback**

#### ✨ Features:
- **Auto-play**: Automatically starts playing recommended songs
- **Playlist Creation**: Generates playlists based on detected emotion
- **30-second Previews**: Uses Spotify's preview URLs
- **Seamless Transitions**: Automatically moves to next track
- **Shuffle Mode**: Randomize playback order
- **Volume Control**: Adjustable volume with mute option
- **Progress Bar**: Visual playback progress with seek functionality

#### 🎵 Player Controls:
- ⏮️ Previous Track
- ▶️/⏸️ Play/Pause
- ⏭️ Next Track
- 🔀 Shuffle
- 🔊 Volume Control

---

## 🚀 How to Use

### **Mode 1: Multi-Modal (Recommended)**

Combine all inputs for maximum accuracy:

1. Click on **Multi-Modal** mode
2. Allow camera and microphone access
3. **Camera**: Your face will be automatically captured
4. **Voice**: Click the record button, speak for 3-5 seconds, click again to stop
5. **Text**: Type how you're feeling (optional)
6. **Heart Rate**: Enter your current heart rate in BPM (optional)
7. Click "**Analyze All & Get Music**"
8. View fusion results showing contribution from each modality
9. Music automatically starts playing!

### **Mode 2: Camera Only**

Quick emotion detection from facial expression:

1. Click **Camera** mode
2. Position your face in the frame
3. Click "**Capture & Analyze**"
4. Get instant emotion detection and music recommendations

### **Mode 3: Voice Only**

Detect emotion from your voice:

1. Click **Voice** mode
2. Click the record button (🔴)
3. Speak naturally for 3-5 seconds
4. Click stop (⏹️)
5. Click "**Analyze Voice**"
6. Get emotion based on voice tone

### **Mode 4: Text Only**

Analyze your written feelings:

1. Click **Text** mode
2. Type your thoughts and feelings
3. Click "**Analyze Text**"
4. Get emotion from sentiment analysis

### **Mode 5: Heart Rate**

Emotion from physiological data:

1. Click **Heart Rate** mode
2. Enter your current heart rate (40-200 BPM)
3. Optional: Connect fitness tracker
4. Click "**Analyze Heart Rate**"
5. Get emotion and wellness recommendations

---

## 🎼 Music Player Features

### **Automatic Playback**
- Toggle **Auto-play** to enable/disable automatic playback
- When enabled, music starts playing immediately after emotion detection
- Automatically transitions between tracks

### **Manual Controls**
- Click any song card to play it immediately
- Use player controls at the bottom:
  - Previous/Next buttons to navigate playlist
  - Play/Pause for playback control
  - Shuffle to randomize playlist order
  - Volume slider for audio level
  - Progress bar to seek within track

### **Playlist Management**
- "Get More Recommendations" button loads additional songs
- Each emotion detection creates a fresh playlist
- Playlist contains 10-15 songs matching your emotion

---

## 🧠 How Multi-Modal Fusion Works

### **Weighted Voting System**

Each modality has a default weight:
- **Face**: 30%
- **Text**: 25%
- **Voice**: 25%
- **Heart Rate**: 20%

The system:
1. Analyzes each available input independently
2. Calculates weighted scores for each emotion
3. Checks consistency across modalities
4. Combines results using intelligent fusion
5. Provides final emotion with high confidence

### **Consistency Scoring**

The system checks if emotions from different modalities align:
- **High consistency** (all agree) → Higher confidence
- **Medium consistency** (some alignment) → Medium confidence
- **Low consistency** (conflicting) → Lower confidence, dominant emotion wins

### **Example**:
```
Face Detection: Happy (85%)
Voice Analysis: Happy (80%)
Text Sentiment: Neutral (70%)
Heart Rate: Excited → Happy (75%)

🎯 Final Result: Happy (88% confidence)
Consistency: High - 3/4 modalities agree
```

---

## 🎨 UI Features

### **Modern Glassmorphism Design**
- Beautiful gradient backgrounds
- Animated floating orbs
- Smooth transitions and micro-animations
- Dark mode optimized

### **Real-time Feedback**
- Status indicators show active inputs
- Visual feedback during recording
- Audio visualizer during voice recording
- Animated heart rate icon

### **Responsive Layout**
- Works on desktop, tablet, and mobile
- Adaptive grid layouts
- Touch-friendly controls

---

## 📊 Emotion-Music Mapping

Each emotion maps to specific music characteristics:

| Emotion | Music Style | Tempo | Energy |
|---------|------------|-------|--------|
| **Happy** | Upbeat, Energetic | 120-140 BPM | High |
| **Sad** | Melancholic, Slow | 60-90 BPM | Low |
| **Angry** | Intense, Heavy | 130-180 BPM | Very High |
| **Fear** | Tense, Uncertain | 100-130 BPM | Medium-High |
| **Surprise** | Dynamic, Unexpected | 110-140 BPM | Medium |
| **Neutral** | Balanced, Ambient | 80-110 BPM | Medium |

---

## 🔬 Technical Architecture

### **Backend** (Python/Flask)
```
app.py
├── /api/detect-emotion (facial analysis)
├── /api/analyze-text (text sentiment)
├── /api/analyze-voice (voice tone)
├── /api/analyze-heart-rate (HR analysis)
├── /api/multimodal-analysis (fusion engine)
├── /api/generate-playlist (auto-playlist)
└── /api/recommend-music (recommendations)
```

### **AI Models**
```
models/
├── emotion_detector.py (CNN for facial emotions)
├── text_analyzer.py (Transformer-based NLP)
├── voice_analyzer.py (Audio feature extraction)
├── heart_rate_analyzer.py (HRV analysis)
├── multimodal_fusion.py (Fusion algorithm)
└── music_recommender.py (Spotify integration)
```

### **Frontend** (JavaScript)
```
static/js/app.js
├── Camera Management
├── Voice Recording (MediaRecorder API)
├── Multi-modal Analysis
├── Music Player
└── Auto-play System
```

---

## 🎯 Benefits of Multi-Modal Detection

1. **Higher Accuracy**: Combining multiple inputs reduces false positives
2. **Robustness**: Works even if one modality fails
3. **Context Awareness**: Better understanding of emotional state
4. **User Choice**: Use what's comfortable (camera, voice, text, or all)
5. **Accessibility**: Multiple input methods for different needs

---

## 🔒 Privacy & Security

- **No Data Storage**: Emotion analysis happens in real-time, no data saved
- **Local Processing**: Face and voice analysis on your machine
- **Spotify API**: Only uses public preview URLs
- **Secure**: All processing through HTTPS
- **Permissions**: Requests camera/mic only when needed

---

## 🎵 Spotify Integration

The system uses Spotify's API to:
- Search for mood-appropriate music
- Get 30-second preview URLs
- Display track name, artist, and album art
- Find songs matching emotional characteristics

**Note**: Only tracks with preview URLs can be played in the browser.

---

## 💡 Tips for Best Results

### **Camera**
- Good lighting on your face
- Look directly at camera
- Natural facial expression

### **Voice**
- Speak naturally for 3-5 seconds
- Quiet environment
- Clear audio

### **Text**
- Be expressive and descriptive
- Use emotional words
- Be honest about feelings

### **Heart Rate**
- Rest for 1 minute before measuring
- Use wearable for accurate data
- Normal adult range: 60-100 BPM

### **Multi-Modal**
- Use at least 2-3 modalities
- More inputs = better accuracy
- Try different combinations

---

## 🐛 Troubleshooting

### Camera Not Working
- Allow camera permissions in browser
- Check if another app is using camera
- Refresh the page

### Microphone Not Working
- Allow microphone permissions
- Check system audio settings
- Try a different browser

### Music Not Playing
- Some tracks don't have previews
- Check internet connection
- Try a different song

### Emotion Detection Incorrect
- Try multi-modal mode
- Ensure good lighting (camera)
- Speak clearly (voice)
- Be descriptive (text)

---

## 🚀 Future Enhancements

- **Real wearable integration** (Apple Watch, Fitbit, etc.)
- **Continuous monitoring** mode
- **Emotion history tracking**
- **Personalized recommendations** based on listening history
- **Full song playback** (requires Spotify Premium)
- **Playlist saving** and sharing
- **Social features** to share moods

---

## 📱 Browser Compatibility

| Browser | Camera | Microphone | Audio Player |
|---------|--------|------------|--------------|
| Chrome | ✅ | ✅ | ✅ |
| Firefox | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ |
| Safari | ✅ | ✅ | ✅ |
| Opera | ✅ | ✅ | ✅ |

**Recommended**: Chrome or Edge for best performance

---

## 🎓 Learn More

- **Emotion Detection**: Uses facial landmarks and CNN
- **Voice Analysis**: Prosody and acoustic features
- **Text Sentiment**: Transformer models (BERT-based)
- **Heart Rate**: HRV analysis for autonomic nervous system
- **Music Therapy**: Science-backed mood-music correlation

---

## 📝 Credits

Built with:
- **TensorFlow** - Deep learning
- **OpenCV** - Computer vision
- **Librosa** - Audio analysis
- **Transformers** - NLP
- **Spotify API** - Music data
- **Flask** - Backend framework

---

## 🎉 Enjoy Your Musical Journey!

Let AI detect your emotions through multiple modalities and discover the perfect soundtrack for your mood!

**Happy Listening! 🎵✨**
