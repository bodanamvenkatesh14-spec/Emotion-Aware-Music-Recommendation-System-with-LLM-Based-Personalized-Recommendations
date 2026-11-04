"""
Heart Rate Based Emotion Detection Module
Analyzes heart rate data from wearables to infer emotional state
"""

import numpy as np
from datetime import datetime

class HeartRateAnalyzer:
    def __init__(self):
        self.emotion_labels = ['Relaxed', 'Happy', 'Excited', 'Stressed', 'Anxious', 'Neutral']
        
        # Heart rate zones and corresponding emotions (based on research)
        # Values are in BPM (beats per minute)
        self.hr_emotion_map = {
            'Relaxed': {'hr_range': (50, 70), 'hrv_range': (50, 100)},
            'Neutral': {'hr_range': (70, 85), 'hrv_range': (40, 80)},
            'Happy': {'hr_range': (75, 95), 'hrv_range': (45, 90)},
            'Excited': {'hr_range': (95, 130), 'hrv_range': (30, 60)},
            'Stressed': {'hr_range': (90, 120), 'hrv_range': (20, 50)},
            'Anxious': {'hr_range': (85, 110), 'hrv_range': (15, 40)}
        }
        
        # Emotion to music emotion mapping
        self.emotion_music_map = {
            'Relaxed': 'Neutral',
            'Happy': 'Happy',
            'Excited': 'Happy',
            'Stressed': 'Sad',
            'Anxious': 'Fear',
            'Neutral': 'Neutral'
        }
    
    def calculate_hrv(self, rr_intervals):
        """
        Calculate Heart Rate Variability (HRV) from RR intervals
        HRV is a key indicator of emotional state and stress levels
        
        Args:
            rr_intervals: list of RR intervals in milliseconds
            
        Returns:
            hrv: Heart Rate Variability score
        """
        if not rr_intervals or len(rr_intervals) < 2:
            return 50  # Default HRV
        
        # RMSSD (Root Mean Square of Successive Differences)
        differences = np.diff(rr_intervals)
        rmssd = np.sqrt(np.mean(differences ** 2))
        
        return rmssd
    
    def analyze_heart_rate(self, heart_rate, hrv=None, rr_intervals=None):
        """
        Analyze heart rate data to detect emotional state
        
        Args:
            heart_rate: Current heart rate in BPM
            hrv: Heart Rate Variability (optional, calculated if rr_intervals provided)
            rr_intervals: RR intervals in milliseconds (optional)
            
        Returns:
            emotion: Detected emotion
            confidence: Confidence score (0-1)
            music_emotion: Mapped emotion for music recommendation
        """
        try:
            # Validate heart rate
            if heart_rate < 40 or heart_rate > 200:
                return 'Neutral', 0.5, 'Neutral'
            
            # Calculate HRV if not provided
            if hrv is None and rr_intervals:
                hrv = self.calculate_hrv(rr_intervals)
            elif hrv is None:
                # Estimate HRV based on HR (inverse relationship)
                hrv = max(20, min(100, 150 - heart_rate))
            
            # Score each emotion based on HR and HRV
            emotion_scores = {}
            
            for emotion, ranges in self.hr_emotion_map.items():
                score = 0
                
                # Heart rate matching
                hr_min, hr_max = ranges['hr_range']
                if hr_min <= heart_rate <= hr_max:
                    score += 0.6
                else:
                    deviation = min(abs(heart_rate - hr_min), abs(heart_rate - hr_max))
                    score += max(0, 0.6 - (deviation / 50))
                
                # HRV matching
                hrv_min, hrv_max = ranges['hrv_range']
                if hrv_min <= hrv <= hrv_max:
                    score += 0.4
                else:
                    deviation = min(abs(hrv - hrv_min), abs(hrv - hrv_max))
                    score += max(0, 0.4 - (deviation / 40))
                
                emotion_scores[emotion] = score
            
            # Additional context-based adjustments
            # High HR + Low HRV = Stress/Anxiety
            if heart_rate > 100 and hrv < 35:
                emotion_scores['Stressed'] *= 1.3
                emotion_scores['Anxious'] *= 1.2
            
            # Low HR + High HRV = Relaxed
            elif heart_rate < 75 and hrv > 60:
                emotion_scores['Relaxed'] *= 1.3
            
            # Moderate HR + Moderate HRV = Happy/Neutral
            elif 70 <= heart_rate <= 90 and 40 <= hrv <= 70:
                emotion_scores['Happy'] *= 1.2
                emotion_scores['Neutral'] *= 1.1
            
            # Find best emotion
            detected_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[detected_emotion], 0.95)
            confidence = max(0.6, confidence)  # Ensure minimum confidence
            
            # Map to music emotion
            music_emotion = self.emotion_music_map.get(detected_emotion, 'Neutral')
            
            return detected_emotion, confidence, music_emotion
            
        except Exception as e:
            print(f"Error analyzing heart rate: {e}")
            return 'Neutral', 0.5, 'Neutral'
    
    def get_emotion_description(self, emotion):
        """Return description of detected emotion from heart rate"""
        descriptions = {
            'Relaxed': 'Your heart rate indicates a relaxed and calm state',
            'Happy': 'Your heart rate shows positive, happy emotions',
            'Excited': 'Your heart rate indicates high excitement and energy',
            'Stressed': 'Your heart rate suggests elevated stress levels',
            'Anxious': 'Your heart rate pattern shows signs of anxiety',
            'Neutral': 'Your heart rate is in a balanced, neutral state'
        }
        return descriptions.get(emotion, 'Heart rate analyzed')
    
    def get_recommendations(self, emotion):
        """Get wellness recommendations based on heart rate emotion"""
        recommendations = {
            'Relaxed': 'Keep enjoying this peaceful state! 🧘',
            'Happy': 'Great vibes! Keep the positive energy flowing! ✨',
            'Excited': 'Channel that energy into something creative! 🎨',
            'Stressed': 'Consider taking deep breaths and listening to calming music 🌊',
            'Anxious': 'Try some relaxation techniques and soothing sounds 🕊️',
            'Neutral': 'You\'re in a balanced state. Perfect for any activity! ⚖️'
        }
        return recommendations.get(emotion, 'Stay healthy! 💚')

# Create global instance
heart_rate_analyzer = HeartRateAnalyzer()
