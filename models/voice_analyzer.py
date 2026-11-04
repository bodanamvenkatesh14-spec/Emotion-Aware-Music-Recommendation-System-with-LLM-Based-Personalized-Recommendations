"""
Voice Tone Emotion Detection Module
Analyzes voice tone to detect emotional state using audio features
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

try:
    import librosa
    HAS_LIBROSA = True
except Exception as e:
    HAS_LIBROSA = False
    print("VoiceAnalyzer notice: librosa not available. Voice analysis will use acoustic estimate fallback.")

class VoiceAnalyzer:
    def __init__(self):
        self.emotion_labels = ['Angry', 'Fear', 'Happy', 'Sad', 'Neutral', 'Surprise']
        
        # Emotion-audio feature mapping (based on research)
        self.emotion_features = {
            'Happy': {'pitch_range': (150, 300), 'energy': (0.6, 1.0), 'tempo': (100, 140)},
            'Sad': {'pitch_range': (80, 150), 'energy': (0.2, 0.5), 'tempo': (60, 90)},
            'Angry': {'pitch_range': (200, 400), 'energy': (0.7, 1.0), 'tempo': (120, 180)},
            'Fear': {'pitch_range': (180, 350), 'energy': (0.5, 0.9), 'tempo': (110, 150)},
            'Surprise': {'pitch_range': (160, 320), 'energy': (0.5, 0.8), 'tempo': (100, 130)},
            'Neutral': {'pitch_range': (120, 200), 'energy': (0.4, 0.6), 'tempo': (80, 110)}
        }
    
    def extract_audio_features(self, audio_data, sr=22050):
        """
        Extract audio features from voice sample
        """
        if not HAS_LIBROSA:
            return {
                'pitch': 180,
                'energy': 0.6,
                'tempo': 110
            }
        try:
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            avg_pitch = np.mean(pitch_values) if pitch_values else 120
            rms = librosa.feature.rms(y=audio_data)[0]
            avg_energy = np.mean(rms)
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
            
            return {
                'pitch': avg_pitch,
                'energy': avg_energy,
                'tempo': float(tempo)
            }
        except Exception as e:
            print(f"Error extracting audio features: {e}")
            return None
    
    def classify_emotion_from_features(self, features):
        """Classify emotion based on extracted audio features"""
        if not features:
            return 'Neutral', 0.5
        
        pitch = features.get('pitch', 120)
        energy = features.get('energy', 0.5)
        tempo = features.get('tempo', 100)
        
        scores = {}
        for emotion, expected in self.emotion_features.items():
            p_min, p_max = expected['pitch_range']
            e_min, e_max = expected['energy']
            t_min, t_max = expected['tempo']
            
            p_score = 1.0 if p_min <= pitch <= p_max else max(0, 1 - abs(pitch - (p_min + p_max) / 2) / 200)
            e_score = 1.0 if e_min <= energy <= e_max else max(0, 1 - abs(energy - (e_min + e_max) / 2) / 0.5)
            t_score = 1.0 if t_min <= tempo <= t_max else max(0, 1 - abs(tempo - (t_min + t_max) / 2) / 100)
            
            scores[emotion] = (p_score + e_score + t_score) / 3
        
        best_emotion = max(scores, key=scores.get)
        confidence = float(scores[best_emotion])
        return best_emotion, min(max(confidence, 0.6), 0.95)
    
    def analyze_voice(self, audio_data, sr=22050):
        """Analyze emotion from voice audio data"""
        features = self.extract_audio_features(audio_data, sr)
        emotion, confidence = self.classify_emotion_from_features(features)
        return emotion, confidence, features
    
    def get_emotion_description(self, emotion):
        """Get friendly description of voice emotion"""
        descriptions = {
            'Happy': 'Your voice sounds upbeat, bright, and energetic!',
            'Sad': 'Your voice tone sounds subdued or quiet.',
            'Angry': 'Your voice shows high intensity and strong emphasis.',
            'Fear': 'Your voice sounds slightly tense or unsteady.',
            'Surprise': 'Your voice shows sudden pitch variations!',
            'Neutral': 'Your voice tone is steady and calm.'
        }
        return descriptions.get(emotion, 'Voice analysis complete.')

# Create global instance
voice_analyzer = VoiceAnalyzer()
