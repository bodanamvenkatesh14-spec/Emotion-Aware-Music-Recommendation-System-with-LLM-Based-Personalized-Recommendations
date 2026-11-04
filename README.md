# 🎵 Emotion-Aware Music Recommendation System

An AI-powered music recommendation system that detects your emotional state through facial expressions and text input, then recommends music to match or improve your mood.

## 🌟 Features

- **Real-time Facial Emotion Detection** - Uses deep learning to detect emotions from webcam
- **Text Sentiment Analysis** - Analyzes text input to understand emotional state
- **Smart Music Recommendations** - Suggests songs based on detected emotions
- **Spotify Integration** - Get personalized playlists from Spotify
- **Beautiful Modern UI** - Stunning glassmorphism design with smooth animations

## 🎭 Supported Emotions

- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😨 Fear
- 😲 Surprise
- 🤢 Disgust
- 😐 Neutral

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **AI/ML**: TensorFlow, Keras, Transformers
- **Computer Vision**: OpenCV
- **NLP**: Hugging Face Transformers
- **Music API**: Spotify API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 📦 Installation

1. **Clone the repository**
```bash
cd emotion-music-ai
```

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up Spotify API**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Copy Client ID and Client Secret
   - Create `.env` file from `.env.example`
   - Add your credentials

5. **Download emotion detection model**
   - The app will automatically download the pre-trained model on first run
   - Or manually download from the releases page

## 🚀 Usage

1. **Start the server**
```bash
python app.py
```

2. **Open your browser**
```
http://localhost:5000
```

3. **Grant camera permissions** when prompted

4. **Let AI detect your emotion** or type how you feel

5. **Get personalized music recommendations!**

## 🏗️ Project Structure

```
emotion-music-ai/
├── app.py                      # Flask application
├── models/
│   ├── emotion_detector.py     # Facial emotion detection
│   ├── text_analyzer.py        # Text sentiment analysis
│   └── music_recommender.py    # Music recommendation engine
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   ├── js/
│   │   └── app.js             # Frontend logic
│   └── models/                # Pre-trained models
├── templates/
│   └── index.html             # Main interface
├── requirements.txt           # Dependencies
└── README.md
```

## 🎯 How It Works

1. **Emotion Detection**: Uses CNN-based model to classify facial expressions
2. **Text Analysis**: Leverages transformer models for sentiment analysis
3. **Recommendation Logic**: Maps emotions to music characteristics (tempo, energy, valence)
4. **Spotify Integration**: Fetches matching tracks from Spotify's vast library

## 🔮 Future Enhancements

- [ ] Voice emotion detection
- [ ] Wearable device integration (heart rate)
- [ ] Mood tracking history and analytics
- [ ] Multi-modal emotion detection (Face + Voice + Text)
- [ ] Therapy-based playlists
- [ ] YouTube Music integration

## 📄 License

MIT License

## 👨‍💻 Author

Built with ❤️ using AI and Machine Learning
