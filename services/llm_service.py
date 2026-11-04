"""
EmotionAI - LLM Service Layer
Handles Emotion Explanations, Music Intent Generation, Wellness Suggestions,
Daily Mood Analytics, and Interactive AI Chat Assistant.
Supports Google Gemini, OpenAI, and a 100% Robust Offline Fallback Engine.
"""

import os
import json
import urllib.request
import urllib.error
import random
from typing import Dict, Any, List, Tuple

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY') or os.getenv('LLM_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        
    def _has_valid_key(self) -> bool:
        return bool(self.api_key and self.api_key.strip() and self.api_key != 'your_llm_api_key_here')

    # ==================== Core LLM Call Handler ====================
    def _call_gemini_api(self, prompt: str, system_instruction: str = "") -> str:
        """Call Google Gemini REST API directly using built-in urllib"""
        if not self._has_valid_key():
            return None
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        
        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"System Context: {system_instruction}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will act according to this context."}]})
            
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                text = res_data['candidates'][0]['content']['parts'][0]['text']
                return text
        except Exception as e:
            print(f"[LLM Service Notice] Gemini API call error: {e}. Using smart fallback.")
            return None

    def _call_openai_api(self, prompt: str, system_instruction: str = "") -> str:
        """Call OpenAI REST API fallback"""
        if not self._has_valid_key():
            return None
            
        url = "https://api.openai.com/v1/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}'
                }
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data['choices'][0]['message']['content']
        except Exception as e:
            print(f"[LLM Service Notice] OpenAI API call error: {e}. Using smart fallback.")
            return None

    def _call_llm(self, prompt: str, system_instruction: str = "") -> str:
        """Dispatch call to active provider"""
        if self.provider == 'openai':
            res = self._call_openai_api(prompt, system_instruction)
            if res: return res
        
        # Default Gemini call
        return self._call_gemini_api(prompt, system_instruction)

    # ==================== 1. Emotion Analysis & Intent ====================
    def generate_emotion_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze multimodal context to produce:
        - Explanation
        - Music Intent (energy, valence, tempo, genres)
        - Wellness Suggestion
        """
        face_emo = context.get('face_emotion', 'Neutral')
        face_conf = context.get('face_confidence', 0.8)
        text_emo = context.get('text_emotion', 'Neutral')
        text_conf = context.get('text_confidence', 0.7)
        overall_emo = context.get('overall_emotion', 'Happy')
        overall_conf = context.get('overall_confidence', 0.85)

        prompt = f"""
Analyze the following user emotion metadata:
- Facial Expression: {face_emo} (Confidence: {int(face_conf*100)}%)
- Text Sentiment: {text_emo} (Confidence: {int(text_conf*100)}%)
- Final Fused Emotion: {overall_emo} (Confidence: {int(overall_conf*100)}%)

Return ONLY a valid JSON object matching this exact schema:
{{
    "explanation": "Short 1-2 sentence non-medical natural language summary of their mood.",
    "suggestion": "Contextual friendly advice or activity suggestion.",
    "music_intent": {{
        "energy": 0.85,
        "valence": 0.90,
        "tempo": 120,
        "genres": ["Telugu", "Pop", "Melody"],
        "mood_description": "uplifting and energetic"
    }}
}}
"""

        system_instruction = "You are EmotionAI, an empathetic emotion-aware music AI assistant. Never provide medical or psychiatric advice."
        raw_text = self._call_llm(prompt, system_instruction)

        if raw_text:
            try:
                # Clean code blocks if present
                clean_text = raw_text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text[7:]
                if clean_text.startswith("```"):
                    clean_text = clean_text[3:]
                if clean_text.endswith("```"):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()
                
                parsed = json.loads(clean_text)
                if 'explanation' in parsed and 'music_intent' in parsed:
                    return parsed
            except Exception as e:
                print(f"[LLM Service Notice] JSON parse error: {e}")

        # Fallback Engine (Runs when API key is absent or network fails)
        return self._generate_fallback_analysis(overall_emo, face_emo, text_emo)

    def _generate_fallback_analysis(self, overall_emo: str, face_emo: str, text_emo: str) -> Dict[str, Any]:
        """Intelligent Rule-Based Fallback Engine"""
        explanations = {
            'Happy': f"Your overall mood is Happy! Your face shows {face_emo} expressions and your text has a positive, upbeat tone.",
            'Sad': f"You seem to be feeling a bit Sad or low in energy today. Our sensors detected {face_emo} cues.",
            'Angry': f"Your current state indicates high energy/intensity (Angry). Facial signals show {face_emo} tension.",
            'Fear': f"You appear to be feeling anxious or stressed. Cues from facial and text signals indicate Fear.",
            'Surprise': f"Something unexpected caught your attention! Cues indicate a state of Surprise.",
            'Disgust': f"Your signals show discomfort or dissatisfaction.",
            'Neutral': f"Your mood is balanced and calm (Neutral). You have a serene baseline state."
        }

        suggestions = {
            'Happy': "Keep the vibrant energy going! Let's play some upbeat Telugu melodies.",
            'Sad': "A gentle Telugu melody may help create a relaxing, comforting space.",
            'Angry': "Try taking a 2-minute deep breath break. Here is some calming music to help reset.",
            'Fear': "Take a moment to unwind. Soothing ambient and classical Telugu tracks are queued for you.",
            'Surprise': "Let's match that spark with dynamic, high-tempo beats!",
            'Disgust': "Clear your thoughts with refreshing instrumental soundscapes.",
            'Neutral': "A perfect focus state. Ideal for lo-fi or acoustic instrumental tracks."
        }

        intents = {
            'Happy': {"energy": 0.85, "valence": 0.90, "tempo": 124, "genres": ["Telugu Pop", "Dance", "Feel-Good"], "mood_description": "uplifting and joyful"},
            'Sad': {"energy": 0.35, "valence": 0.30, "tempo": 75, "genres": ["Telugu Melody", "Acoustic", "Soulful"], "mood_description": "soft and comforting"},
            'Angry': {"energy": 0.92, "valence": 0.40, "tempo": 135, "genres": ["Rock", "Intense Telugu Beats", "Fast Rhythm"], "mood_description": "high energy and intense"},
            'Fear': {"energy": 0.25, "valence": 0.50, "tempo": 65, "genres": ["Ambient", "Telugu Classical", "Calm Strings"], "mood_description": "soothing and peaceful"},
            'Surprise': {"energy": 0.75, "valence": 0.80, "tempo": 115, "genres": ["Experimental", "Telugu Dance", "Synthpop"], "mood_description": "dynamic and vibrant"},
            'Disgust': {"energy": 0.45, "valence": 0.55, "tempo": 90, "genres": ["Chillout", "Lo-Fi", "Telugu Instrumental"], "mood_description": "refreshing and clear"},
            'Neutral': {"energy": 0.50, "valence": 0.60, "tempo": 95, "genres": ["Telugu Acoustic", "Indie", "Focus Beats"], "mood_description": "balanced and steady"}
        }

        return {
            "explanation": explanations.get(overall_emo, explanations['Neutral']),
            "suggestion": suggestions.get(overall_emo, suggestions['Neutral']),
            "music_intent": intents.get(overall_emo, intents['Neutral'])
        }

    # ==================== 2. Interactive AI Chat Assistant ====================
    def chat_with_emotion_context(self, user_message: str, context: Dict[str, Any]) -> str:
        """Handle interactive chat with user emotion context"""
        current_emo = context.get('overall_emotion', 'Happy')
        prev_emo = context.get('previous_emotion', 'Neutral')
        liked_tracks = context.get('liked_tracks', [])
        current_track = context.get('current_track', 'Rage Against the Machine - Killing in the Name')

        prompt = f"""
User Message: "{user_message}"

Current User Context:
- Current Mood: {current_emo}
- Previous Mood: {prev_emo}
- Currently Playing: {current_track}
- Liked Songs: {', '.join(liked_tracks) if liked_tracks else 'None yet'}

Respond as EmotionAI, a friendly, empathetic music assistant. Keep response under 3 sentences.
"""

        system_instruction = "You are EmotionAI Assistant. Answer music questions using their current emotion context."
        raw_text = self._call_llm(prompt, system_instruction)

        if raw_text:
            return raw_text.strip()

        # Fallback Chat Responses for instant interactive response without API keys
        msg = user_message.lower()
        if "why did you recommend" in msg or "why this song" in msg:
            return f"I recommended this track because your current mood is **{current_emo}**! We selected music with matching energy and rhythm."
        elif "happy telugu" in msg or "telugu songs" in msg or "recommend" in msg:
            return f"Since you're feeling **{current_emo}**, I've curated top Telugu tracks like *Bullet Song*, *Ramuloo Ramulaa*, and upbeat melodies for you!"
        elif "stressed" in msg or "anxious" in msg or "sad" in msg:
            return "I hear you. Let's switch to soothing Telugu acoustic melodies to create a peaceful atmosphere for you."
        elif "mood change" in msg or "changed today" in msg:
            return f"Your mood shifted from **{prev_emo}** → **{current_emo}**. Our sensors continuously track your signals to adapt the music!"
        elif "most common" in msg or "common mood" in msg:
            return f"Based on today's analytics, your predominant mood has been **{current_emo}**."
        else:
            return f"I'm here for you! Currently tuning into your **{current_emo}** vibe. Feel free to ask for specific Telugu songs or playlists!"

    # ==================== 3. Mood Shift Explanation ====================
    def generate_mood_shift_explanation(self, prev_emo: str, curr_emo: str) -> str:
        """Generate short summary when mood changes"""
        prompt = f"The user's mood changed from {prev_emo} to {curr_emo}. Write a 1-sentence friendly observation."
        res = self._call_llm(prompt)
        if res:
            return res.strip()
            
        return f"Your mood shifted from {prev_emo} to {curr_emo}. We updated your music playlist accordingly!"

    # ==================== 4. Daily Analytics Summary ====================
    def generate_daily_mood_summary(self, summary_data: Dict[str, float]) -> str:
        """Generate daily analytical insight"""
        formatted = ", ".join([f"{k}: {v}%" for k, v in summary_data.items()])
        prompt = f"Given today's emotion distribution ({formatted}), generate a 2-sentence summary of the user's emotional day."
        res = self._call_llm(prompt)
        if res:
            return res.strip()
            
        top_emo = max(summary_data, key=summary_data.get) if summary_data else "Happy"
        return f"You experienced mostly positive energy today with {top_emo} being your primary mood. Your mood remained vibrant throughout the day!"

# Global Singleton Instance
llm_service = LLMService()
