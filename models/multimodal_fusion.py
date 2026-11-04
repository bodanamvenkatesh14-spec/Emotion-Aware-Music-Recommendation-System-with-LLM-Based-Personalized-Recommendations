"""
Multi-Modal Emotion Fusion Engine
Combines multiple emotion detection modalities for improved accuracy
"""

import numpy as np
from collections import Counter

class MultiModalFusion:
    def __init__(self):
        # Standard emotion labels across all modalities
        self.standard_emotions = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Neutral']
        
        # Modality weights (can be adjusted based on reliability)
        self.default_weights = {
            'face': 0.30,      # Facial expression
            'text': 0.25,      # Text sentiment
            'voice': 0.25,     # Voice tone
            'heart_rate': 0.20 # Heart rate data
        }
        
        # Emotion compatibility matrix (how well emotions from different modalities align)
        self.emotion_compatibility = {
            'Happy': ['Happy', 'Surprise', 'Neutral'],
            'Sad': ['Sad', 'Fear', 'Neutral'],
            'Angry': ['Angry', 'Disgust', 'Fear'],
            'Fear': ['Fear', 'Sad', 'Surprise'],
            'Surprise': ['Surprise', 'Happy', 'Fear'],
            'Neutral': ['Neutral', 'Happy', 'Sad'],
            'Disgust': ['Angry', 'Sad', 'Neutral'],
            'Relaxed': ['Happy', 'Neutral'],
            'Excited': ['Happy', 'Surprise'],
            'Stressed': ['Angry', 'Sad', 'Fear'],
            'Anxious': ['Fear', 'Sad']
        }
    
    def normalize_emotion(self, emotion):
        """
        Normalize emotion labels from different modalities to standard set
        """
        emotion_mapping = {
            'Relaxed': 'Neutral',
            'Excited': 'Happy',
            'Stressed': 'Angry',
            'Anxious': 'Fear',
            'Disgust': 'Angry'
        }
        
        return emotion_mapping.get(emotion, emotion)
    
    def calculate_emotion_consistency(self, emotions):
        """
        Calculate how consistent the emotions are across modalities
        Higher score = more consistent = higher confidence
        """
        if len(emotions) < 2:
            return 1.0
        
        # Normalize all emotions
        normalized = [self.normalize_emotion(e) for e in emotions]
        
        # Check compatibility
        compatibility_scores = []
        for i, emotion1 in enumerate(normalized):
            for emotion2 in normalized[i+1:]:
                if emotion1 == emotion2:
                    compatibility_scores.append(1.0)
                elif emotion2 in self.emotion_compatibility.get(emotion1, []):
                    compatibility_scores.append(0.7)
                else:
                    compatibility_scores.append(0.3)
        
        return np.mean(compatibility_scores) if compatibility_scores else 0.5
    
    def weighted_fusion(self, emotion_data, custom_weights=None):
        """
        Fuse emotions using weighted voting
        
        Args:
            emotion_data: dict with modality as key, (emotion, confidence) as value
                         Example: {'face': ('Happy', 0.85), 'text': ('Happy', 0.90)}
            custom_weights: optional custom weights for modalities
            
        Returns:
            final_emotion: fused emotion label
            final_confidence: confidence score
            modality_contributions: breakdown of each modality's contribution
        """
        if not emotion_data:
            return 'Neutral', 0.5, {}
        
        weights = custom_weights if custom_weights else self.default_weights
        
        # Normalize weights for only available modalities
        available_modalities = set(emotion_data.keys())
        total_weight = sum(weights.get(m, 0) for m in available_modalities)
        
        if total_weight == 0:
            return 'Neutral', 0.5, {}
        
        normalized_weights = {
            m: weights.get(m, 0) / total_weight 
            for m in available_modalities
        }
        
        # Calculate weighted scores for each emotion
        emotion_scores = {}
        modality_contributions = {}
        
        for modality, (emotion, confidence) in emotion_data.items():
            normalized_emotion = self.normalize_emotion(emotion)
            weight = normalized_weights.get(modality, 0)
            contribution = confidence * weight
            
            if normalized_emotion not in emotion_scores:
                emotion_scores[normalized_emotion] = 0
            
            emotion_scores[normalized_emotion] += contribution
            modality_contributions[modality] = {
                'emotion': emotion,
                'confidence': confidence,
                'weight': weight,
                'contribution': contribution
            }
        
        # Find emotion with highest score
        if not emotion_scores:
            return 'Neutral', 0.5, modality_contributions
        
        final_emotion = max(emotion_scores, key=emotion_scores.get)
        base_confidence = emotion_scores[final_emotion]
        
        # Adjust confidence based on consistency
        all_emotions = [data[0] for data in emotion_data.values()]
        consistency = self.calculate_emotion_consistency(all_emotions)
        
        # Final confidence is weighted by consistency
        final_confidence = (base_confidence * 0.7) + (consistency * 0.3)
        final_confidence = min(0.98, max(0.6, final_confidence))  # Clamp between 60% and 98%
        
        return final_emotion, final_confidence, modality_contributions
    
    def majority_voting(self, emotion_data):
        """
        Simple majority voting fusion (alternative to weighted fusion)
        """
        if not emotion_data:
            return 'Neutral', 0.5
        
        # Normalize emotions
        emotions = [self.normalize_emotion(e[0]) for e in emotion_data.values()]
        
        # Count votes
        emotion_counts = Counter(emotions)
        most_common_emotion = emotion_counts.most_common(1)[0][0]
        
        # Calculate confidence based on agreement
        agreement_ratio = emotion_counts[most_common_emotion] / len(emotions)
        avg_confidence = np.mean([conf for _, conf in emotion_data.values()])
        
        final_confidence = (agreement_ratio * 0.5) + (avg_confidence * 0.5)
        
        return most_common_emotion, final_confidence
    
    def get_fusion_summary(self, emotion_data, final_emotion, final_confidence, contributions):
        """
        Generate a human-readable summary of the fusion process
        """
        summary = {
            'num_modalities': len(emotion_data),
            'modalities_used': list(emotion_data.keys()),
            'final_emotion': final_emotion,
            'final_confidence': round(final_confidence, 2),
            'individual_detections': {},
            'consistency_score': round(
                self.calculate_emotion_consistency([e[0] for e in emotion_data.values()]), 
                2
            )
        }
        
        for modality, data in emotion_data.items():
            summary['individual_detections'][modality] = {
                'emotion': data[0],
                'confidence': round(data[1], 2)
            }
        
        return summary
    
    def analyze_multimodal(self, face_data=None, text_data=None, voice_data=None, hr_data=None):
        """
        Main method to analyze all available modalities and fuse results
        
        Args:
            face_data: (emotion, confidence) from facial detection
            text_data: (emotion, confidence) from text analysis
            voice_data: (emotion, confidence) from voice analysis
            hr_data: (emotion, confidence, music_emotion) from heart rate analysis
            
        Returns:
            final_emotion, confidence, detailed_summary
        """
        emotion_data = {}
        
        if face_data and face_data[0]:
            emotion_data['face'] = face_data
        
        if text_data and text_data[0]:
            emotion_data['text'] = text_data
        
        if voice_data and voice_data[0]:
            emotion_data['voice'] = voice_data
        
        if hr_data and hr_data[0]:
            # Use the music-mapped emotion from heart rate
            if len(hr_data) >= 3:
                emotion_data['heart_rate'] = (hr_data[2], hr_data[1])  # music_emotion, confidence
            else:
                emotion_data['heart_rate'] = hr_data
        
        # Perform weighted fusion
        final_emotion, final_confidence, contributions = self.weighted_fusion(emotion_data)
        
        # Generate summary
        summary = self.get_fusion_summary(
            emotion_data, 
            final_emotion, 
            final_confidence, 
            contributions
        )
        
        return final_emotion, final_confidence, summary

# Create global instance
multimodal_fusion = MultiModalFusion()
