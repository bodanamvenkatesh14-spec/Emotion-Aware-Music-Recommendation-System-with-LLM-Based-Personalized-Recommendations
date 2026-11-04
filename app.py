"""
Emotion-Aware Music Recommendation System - Flask Backend
"""

from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
import sqlite3
import datetime
from dotenv import load_dotenv

# Import our AI models & LLM service
from models.emotion_detector import emotion_detector
from models.text_analyzer import text_analyzer
from models.music_recommender import music_recommender
from models.voice_analyzer import voice_analyzer
from models.heart_rate_analyzer import heart_rate_analyzer
from models.multimodal_fusion import multimodal_fusion
from services.llm_service import llm_service

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Database Setup
def init_db():
    conn = sqlite3.connect('emotion_db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS emotion_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  emotion TEXT, 
                  confidence REAL, 
                  modality TEXT, 
                  llm_response TEXT,
                  suggestion TEXT,
                  music_intent TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS liked_tracks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  track_name TEXT,
                  artist TEXT,
                  action TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  user_message TEXT,
                  bot_response TEXT,
                  emotion TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('emotion_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

SMART_SUGGESTIONS = {
    'Happy': 'Keep the good vibes going! How about an upbeat track?',
    'Sad': 'Take a deep breath. Would you like some relaxing music?',
    'Angry': 'Try a 2-minute breathing exercise. We have some calming tracks for you.',
    'Fear': 'You are safe here. Let us play some soothing ambient sounds.',
    'Surprise': 'Oh! Let us match that energy with something unexpected!',
    'Disgust': 'Let us clear your mind with some refreshing tunes.',
    'Neutral': 'A perfect blank canvas. How about some focus music?'
}

def save_emotion_and_get_change(user_id, emotion, confidence, modality):
    if not user_id:
        return None
    try:
        conn = get_db_connection()
        last_entry = conn.execute('''
            SELECT emotion FROM emotion_history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        ''', (user_id,)).fetchone()
        
        conn.execute('''
            INSERT INTO emotion_history (user_id, emotion, confidence, modality) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, emotion, confidence, modality))
        conn.commit()
        conn.close()
        
        if last_entry and last_entry['emotion'] != emotion:
            return f"Your mood changed from {last_entry['emotion']} → {emotion}"
    except Exception as e:
        print(f"Error saving emotion: {e}")
    return None

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT id, username FROM users WHERE username = ?', (username,)).fetchone()
    
    if not user:
        conn.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        user = conn.execute('SELECT id, username FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return jsonify({'success': True, 'user_id': user['id'], 'username': user['username']})

@app.route('/api/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
        
    conn = get_db_connection()
    history = conn.execute('''
        SELECT emotion, confidence, modality, timestamp 
        FROM emotion_history 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 100
    ''', (user_id,)).fetchall()
    
    # Get daily summary percentages
    summary_raw = conn.execute('''
        SELECT emotion, COUNT(*) as count 
        FROM emotion_history 
        WHERE user_id = ? AND date(timestamp) = date('now')
        GROUP BY emotion
    ''', (user_id,)).fetchall()
    conn.close()
    
    summary = {}
    total = sum([row['count'] for row in summary_raw])
    if total > 0:
        for row in summary_raw:
            summary[row['emotion']] = round((row['count'] / total) * 100, 1)
            
    return jsonify({
        'success': True,
        'history': [dict(h) for h in history],
        'daily_summary': summary
    })

@app.route('/api/like_track', methods=['POST'])
def like_track():
    data = request.json
    user_id = data.get('user_id')
    track_name = data.get('track_name')
    artist = data.get('artist', '')
    action = data.get('action') # like or dislike
    
    if not all([user_id, track_name, action]):
        return jsonify({'error': 'Missing data'}), 400
        
    conn = get_db_connection()
    conn.execute('INSERT INTO liked_tracks (user_id, track_name, artist, action) VALUES (?, ?, ?, ?)',
                 (user_id, track_name, artist, action))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/llm/emotion-analysis', methods=['POST'])
def llm_emotion_analysis():
    """
    Generate LLM-powered emotion explanation, wellness suggestion, and music intent
    """
    try:
        data = request.json or {}
        analysis = llm_service.generate_emotion_analysis(data)
        return jsonify({
            'success': True,
            'emotion': data.get('overall_emotion', 'Happy'),
            'explanation': analysis.get('explanation', ''),
            'suggestion': analysis.get('suggestion', ''),
            'music_intent': analysis.get('music_intent', {})
        })
    except Exception as e:
        print(f"Error in LLM emotion analysis route: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/music-intent', methods=['POST'])
def llm_music_intent():
    """
    Generate structured music intent for a given emotion context
    """
    try:
        data = request.json or {}
        analysis = llm_service.generate_emotion_analysis(data)
        return jsonify({
            'success': True,
            'music_intent': analysis.get('music_intent', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/chat', methods=['POST'])
def llm_chat():
    """
    Interactive AI Chat Assistant route
    """
    try:
        data = request.json or {}
        user_message = data.get('message', '')
        user_id = data.get('user_id')
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
            
        bot_response = llm_service.chat_with_emotion_context(user_message, context)
        
        if user_id:
            try:
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO chat_history (user_id, user_message, bot_response, emotion) VALUES (?, ?, ?, ?)',
                    (user_id, user_message, bot_response, context.get('overall_emotion', 'Neutral'))
                )
                conn.commit()
                conn.close()
            except Exception as dbe:
                print(f"Chat log DB notice: {dbe}")

        return jsonify({
            'success': True,
            'response': bot_response,
            'user_message': user_message
        })
    except Exception as e:
        print(f"Error in LLM chat route: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/daily-summary', methods=['GET'])
def llm_daily_summary():
    """
    Generate LLM-driven daily mood analytics summary
    """
    try:
        user_id = request.args.get('user_id')
        conn = get_db_connection()
        summary_raw = conn.execute('''
            SELECT emotion, COUNT(*) as count 
            FROM emotion_history 
            WHERE user_id = ? AND date(timestamp) = date('now')
            GROUP BY emotion
        ''', (user_id,)).fetchall() if user_id else []
        conn.close()
        
        summary = {}
        total = sum([row['count'] for row in summary_raw])
        if total > 0:
            for row in summary_raw:
                summary[row['emotion']] = round((row['count'] / total) * 100, 1)
                
        insight = llm_service.generate_daily_mood_summary(summary)
        
        return jsonify({
            'success': True,
            'daily_summary': summary,
            'llm_insight': insight
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize models on startup
print("\nInitializing Emotion-Aware Music Recommendation System...")
print("=" * 60)

# Load emotion detector
emotion_detector.load_model()

# Load text analyzer
text_analyzer.load_model()

# Connect to Spotify
music_recommender.connect_spotify()

print("=" * 60)
print("[OK] System ready!\n")

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/detect-emotion', methods=['POST'])
def detect_emotion():
    """
    Detect emotion from webcam image
    Expects: base64 encoded image
    Returns: emotion, confidence, emoji
    """
    try:
        data = request.json
        image_data = data.get('image', '')
        user_id = data.get('user_id')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect emotion
        emotion, confidence, face_coords = emotion_detector.predict_emotion(frame)
        
        if emotion is None:
            return jsonify({
                'success': False,
                'message': 'No face detected. Please ensure your face is visible.'
            })
        
        emoji = emotion_detector.get_emotion_emoji(emotion)
        
        mood_change = save_emotion_and_get_change(user_id, emotion, float(confidence), 'Face')
        suggestion = SMART_SUGGESTIONS.get(emotion, '')
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': float(confidence),
            'emoji': emoji,
            'face_detected': True,
            'mood_change': mood_change,
            'suggestion': suggestion
        })
        
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """
    Analyze emotion from text input
    Expects: text string
    Returns: emotion, confidence, description
    """
    try:
        data = request.json
        text = data.get('text', '')
        user_id = data.get('user_id')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze emotion
        emotion, confidence = text_analyzer.analyze_text(text)
        description = text_analyzer.get_emotion_description(emotion)
        emoji = emotion_detector.get_emotion_emoji(emotion)
        
        mood_change = save_emotion_and_get_change(user_id, emotion, float(confidence), 'Text')
        suggestion = SMART_SUGGESTIONS.get(emotion, '')
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': float(confidence),
            'description': description,
            'emoji': emoji,
            'mood_change': mood_change,
            'suggestion': suggestion
        })
        
    except Exception as e:
        print(f"Error in text analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend-music', methods=['POST'])
def recommend_music():
    """
    Get music recommendations based on emotion
    Expects: emotion
    Returns: list of recommended tracks
    """
    try:
        data = request.json
        emotion = data.get('emotion', 'Neutral')
        limit = data.get('limit', 10)
        
        # Get recommendations
        recommendations = music_recommender.get_recommendations(emotion, limit)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Error in music recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/emotion/<emotion>', methods=['GET'])
def music_by_emotion(emotion):
    """
    Get primary track for a given emotion.
    Returns track info + audio path (null if file not available).
    Example: GET /api/music/emotion/Happy
    """
    try:
        tracks = music_recommender.get_recommendations(emotion, limit=1)
        if not tracks:
            return jsonify({'success': False, 'message': 'No track found for this emotion'}), 404

        track = tracks[0]
        emoji_map = {
            'Happy': '😊', 'Sad': '😢', 'Angry': '😡',
            'Fear': '😨', 'Surprise': '😲', 'Disgust': '🤢', 'Neutral': '😐'
        }

        audio_url = track.get('url') if track.get('source') == 'local' else None
        response = {
            'success': True,
            'emotion': emotion,
            'emoji': emoji_map.get(emotion, '😐'),
            'track': track.get('name', ''),
            'artist': track.get('artist', ''),
            'audio': audio_url,
            'source': track.get('source', 'online'),
        }
        if not audio_url:
            response['message'] = 'Audio file not available'

        return jsonify(response)
    except Exception as e:
        print(f"Error in music_by_emotion: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/combined-analysis', methods=['POST'])
def combined_analysis():
    """
    Analyze both image and text, then recommend music
    Expects: image (optional), text (optional)
    Returns: emotion, recommendations
    """
    try:
        data = request.json
        image_data = data.get('image')
        text = data.get('text')
        user_id = data.get('user_id')
        
        emotions = []
        confidences = []
        modality_breakdown = {}
        
        # Analyze image if provided
        if image_data:
            image_data = image_data.split(',')[1] if ',' in image_data else image_data
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            emotion, confidence, _ = emotion_detector.predict_emotion(frame)
            if emotion:
                emotions.append(emotion)
                confidences.append(confidence)
                modality_breakdown['Face'] = {'emotion': emotion, 'confidence': float(confidence)}
        
        # Analyze text if provided
        if text:
            emotion, confidence = text_analyzer.analyze_text(text)
            emotions.append(emotion)
            confidences.append(confidence)
            modality_breakdown['Text'] = {'emotion': emotion, 'confidence': float(confidence)}
        
        # Determine final emotion (weighted by confidence)
        if emotions:
            # Choose emotion with highest confidence
            max_idx = confidences.index(max(confidences))
            final_emotion = emotions[max_idx]
            final_confidence = confidences[max_idx]
        else:
            final_emotion = 'Neutral'
            final_confidence = 0.5
        
        # Get music recommendations
        recommendations = music_recommender.get_recommendations(final_emotion, 10)
        emoji = emotion_detector.get_emotion_emoji(final_emotion)
        
        mood_change = save_emotion_and_get_change(user_id, final_emotion, float(final_confidence), 'Combined')
        suggestion = SMART_SUGGESTIONS.get(final_emotion, '')
        
        return jsonify({
            'success': True,
            'emotion': final_emotion,
            'confidence': float(final_confidence),
            'emoji': emoji,
            'recommendations': recommendations,
            'modality_breakdown': modality_breakdown,
            'mood_change': mood_change,
            'suggestion': suggestion
        })
        
    except Exception as e:
        print(f"Error in combined analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-voice', methods=['POST'])
def analyze_voice():
    """
    Analyze emotion from voice audio
    Expects: audio data (base64 encoded WAV/MP3)
    Returns: emotion, confidence, features
    """
    try:
        import io
        import soundfile as sf
        
        data = request.json
        audio_data = data.get('audio', '')
        
        if not audio_data:
            return jsonify({'error': 'No audio provided'}), 400
        
        # Decode base64 audio
        audio_data = audio_data.split(',')[1] if ',' in audio_data else audio_data
        audio_bytes = base64.b64decode(audio_data)
        
        # Load audio using soundfile
        audio_array, sample_rate = sf.read(io.BytesIO(audio_bytes))
        
        # Convert stereo to mono if needed
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)
        
        # Analyze voice
        emotion, confidence, features = voice_analyzer.analyze_voice(audio_array, sample_rate)
        description = voice_analyzer.get_emotion_description(emotion)
        emoji = emotion_detector.get_emotion_emoji(emotion)
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': float(confidence),
            'description': description,
            'emoji': emoji,
            'features': {
                'pitch': float(features['pitch']) if features else 0,
                'energy': float(features['energy']) if features else 0,
                'tempo': float(features['tempo']) if features else 0
            } if features else None
        })
        
    except Exception as e:
        print(f"Error in voice analysis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-heart-rate', methods=['POST'])
def analyze_heart_rate():
    """
    Analyze emotion from heart rate data
    Expects: heart_rate (BPM), hrv (optional), rr_intervals (optional)
    Returns: emotion, confidence, recommendations
    """
    try:
        data = request.json
        heart_rate = data.get('heart_rate')
        hrv = data.get('hrv')
        rr_intervals = data.get('rr_intervals')
        
        if not heart_rate:
            return jsonify({'error': 'No heart rate data provided'}), 400
        
        # Analyze heart rate
        emotion, confidence, music_emotion = heart_rate_analyzer.analyze_heart_rate(
            heart_rate, hrv, rr_intervals
        )
        
        description = heart_rate_analyzer.get_emotion_description(emotion)
        recommendations = heart_rate_analyzer.get_recommendations(emotion)
        emoji = emotion_detector.get_emotion_emoji(music_emotion)
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'music_emotion': music_emotion,
            'confidence': float(confidence),
            'description': description,
            'recommendations': recommendations,
            'emoji': emoji
        })
        
    except Exception as e:
        print(f"Error in heart rate analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/multimodal-analysis', methods=['POST'])
def multimodal_analysis():
    """
    Multi-modal emotion detection combining all available inputs
    Expects: image, text, audio, heart_rate (all optional but at least one required)
    Returns: fused emotion, confidence, breakdown by modality
    """
    try:
        import io
        import soundfile as sf
        
        data = request.json
        image_data = data.get('image')
        text = data.get('text')
        audio_data = data.get('audio')
        heart_rate = data.get('heart_rate')
        hrv = data.get('hrv')
        
        # Results from each modality
        face_result = None
        text_result = None
        voice_result = None
        hr_result = None
        
        # Analyze facial expression
        if image_data:
            try:
                image_data_clean = image_data.split(',')[1] if ',' in image_data else image_data
                image_bytes = base64.b64decode(image_data_clean)
                nparr = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                emotion, confidence, _ = emotion_detector.predict_emotion(frame)
                if emotion:
                    face_result = (emotion, confidence)
            except Exception as e:
                print(f"Face analysis error: {e}")
        
        # Analyze text sentiment
        if text:
            try:
                emotion, confidence = text_analyzer.analyze_text(text)
                text_result = (emotion, confidence)
            except Exception as e:
                print(f"Text analysis error: {e}")
        
        # Analyze voice tone
        if audio_data:
            try:
                audio_data_clean = audio_data.split(',')[1] if ',' in audio_data else audio_data
                audio_bytes = base64.b64decode(audio_data_clean)
                audio_array, sample_rate = sf.read(io.BytesIO(audio_bytes))
                
                if len(audio_array.shape) > 1:
                    audio_array = np.mean(audio_array, axis=1)
                
                emotion, confidence, _ = voice_analyzer.analyze_voice(audio_array, sample_rate)
                voice_result = (emotion, confidence)
            except Exception as e:
                print(f"Voice analysis error: {e}")
        
        # Analyze heart rate
        if heart_rate:
            try:
                emotion, confidence, music_emotion = heart_rate_analyzer.analyze_heart_rate(
                    heart_rate, hrv
                )
                hr_result = (emotion, confidence, music_emotion)
            except Exception as e:
                print(f"Heart rate analysis error: {e}")
        
        # Fuse all results
        final_emotion, final_confidence, summary = multimodal_fusion.analyze_multimodal(
            face_result, text_result, voice_result, hr_result
        )
        
        # Get music recommendations
        recommendations = music_recommender.get_recommendations(final_emotion, 15)
        emoji = emotion_detector.get_emotion_emoji(final_emotion)
        
        return jsonify({
            'success': True,
            'emotion': final_emotion,
            'confidence': float(final_confidence),
            'emoji': emoji,
            'summary': summary,
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Error in multimodal analysis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-playlist', methods=['POST'])
def generate_playlist():
    """
    Generate an automatic playlist based on emotion
    Supports autoplay feature by returning songs in sequence
    Expects: emotion, duration (minutes), shuffle
    Returns: playlist with songs
    """
    try:
        data = request.json
        emotion = data.get('emotion', 'Neutral')
        duration = data.get('duration', 30)  # Default 30 minutes
        shuffle = data.get('shuffle', False)
        
        # Calculate number of songs (avg 3.5 min per song)
        num_songs = max(5, int(duration / 3.5))
        
        # Get recommendations
        recommendations = music_recommender.get_recommendations(emotion, num_songs)
        
        # Shuffle if requested
        if shuffle:
            import random
            random.shuffle(recommendations)
        
        return jsonify({
            'success': True,
            'playlist': recommendations,
            'emotion': emotion,
            'total_songs': len(recommendations),
            'estimated_duration': len(recommendations) * 3.5
        })
        
    except Exception as e:
        print(f"Error generating playlist: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models': {
            'emotion_detector': emotion_detector.model is not None,
            'text_analyzer': text_analyzer.sentiment_analyzer is not None,
            'spotify': music_recommender.sp is not None
        }
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/models', exist_ok=True)
    
    # Run Flask app
    print("\nStarting server...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
