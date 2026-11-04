"""
Text-based Emotion/Sentiment Analysis Module
Uses NLP or Keyword Fallback to analyze emotional content in text
"""

import re

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except Exception as e:
    HAS_TRANSFORMERS = False
    print("Transformers notice: Hugging Face transformers not installed. Using keyword sentiment fallback.")

class TextAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = None
        self.emotion_keywords = {
            'Happy': ['happy', 'joy', 'excited', 'amazing', 'wonderful', 'great', 'love', 
                     'excellent', 'fantastic', 'good', 'glad', 'cheerful', 'delighted'],
            'Sad': ['sad', 'depressed', 'unhappy', 'miserable', 'down', 'lonely', 
                   'heartbroken', 'upset', 'disappointed', 'blue', 'gloomy'],
            'Angry': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 
                     'rage', 'outraged', 'hate', 'pissed'],
            'Fear': ['scared', 'afraid', 'terrified', 'anxious', 'worried', 'nervous', 
                    'fearful', 'panic', 'stress', 'overwhelmed'],
            'Surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected', 
                        'wow', 'incredible'],
            'Neutral': ['okay', 'fine', 'neutral', 'normal', 'alright', 'nothing']
        }
        
    def load_model(self):
        """Load sentiment analysis model"""
        if not HAS_TRANSFORMERS:
            print("[OK] Text analyzer running in Keyword Sentiment Fallback Mode.")
            return

        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            print("[OK] Text sentiment analyzer loaded successfully")
        except Exception as e:
            print(f"[NOTICE] Error loading sentiment analyzer: {e}")
            self.sentiment_analyzer = None
    
    def keyword_based_emotion(self, text):
        """Fallback emotion detection using keywords"""
        text_lower = text.lower()
        emotion_scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1
        
        # Get emotion with highest score
        if max(emotion_scores.values()) > 0:
            emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[emotion] * 0.3, 0.95)
            return emotion, confidence
        
        return 'Neutral', 0.5
    
    def analyze_text(self, text):
        """
        Analyze emotion from text input
        Returns: emotion, confidence
        """
        if not text or len(text.strip()) < 3:
            return 'Neutral', 0.5
        
        # Try keyword-based detection first (more specific emotions)
        emotion, confidence = self.keyword_based_emotion(text)
        
        if confidence > 0.3:
            return emotion, confidence
        
        # If model is available, use it for sentiment
        if self.sentiment_analyzer:
            try:
                result = self.sentiment_analyzer(text[:512])[0]
                sentiment = result['label']
                score = result['score']
                
                # Map sentiment to emotion
                if sentiment == 'POSITIVE':
                    return 'Happy', score
                elif sentiment == 'NEGATIVE':
                    return 'Sad', score
                else:
                    return 'Neutral', score
            except Exception as e:
                print(f"Error in sentiment analysis: {e}")
        
        return emotion, confidence
    
    def get_emotion_description(self, emotion):
        """Get a friendly description of the emotion"""
        descriptions = {
            'Happy': 'You seem to be feeling positive and upbeat!',
            'Sad': 'You might be feeling a bit down or melancholic.',
            'Angry': 'You appear to be frustrated or upset.',
            'Fear': 'You seem anxious or worried about something.',
            'Surprise': 'Something unexpected caught your attention!',
            'Disgust': 'You seem displeased or uncomfortable.',
            'Neutral': 'You\'re feeling calm and balanced.'
        }
        return descriptions.get(emotion, 'Your emotional state is being analyzed.')

# Create global instance
text_analyzer = TextAnalyzer()
