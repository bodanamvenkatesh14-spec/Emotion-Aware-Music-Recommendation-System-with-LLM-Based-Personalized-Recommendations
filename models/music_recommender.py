"""
Music Recommendation Engine
Recommends music based on detected emotions & LLM music intent using Spotify API / Curated Telugu Track DB.
NO local MP3 files required — uses authorized online previews, YouTube embeds, and Spotify web links.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import random

load_dotenv()

class MusicRecommender:
    def __init__(self):
        self.sp = None
        
        # Audio feature parameters mapping
        self.emotion_to_music_params = {
            'Happy': {
                'target_valence': 0.85,
                'target_energy': 0.80,
                'target_tempo': 124,
                'description': 'upbeat and energetic Telugu tracks'
            },
            'Sad': {
                'target_valence': 0.30,
                'target_energy': 0.35,
                'target_tempo': 75,
                'description': 'calm and soothing Telugu melodies'
            },
            'Angry': {
                'target_valence': 0.40,
                'target_energy': 0.92,
                'target_tempo': 135,
                'description': 'intense and powerful mass beats'
            },
            'Fear': {
                'target_valence': 0.45,
                'target_energy': 0.25,
                'target_tempo': 65,
                'description': 'relaxing ambient Telugu classical tracks'
            },
            'Surprise': {
                'target_valence': 0.75,
                'target_energy': 0.70,
                'target_tempo': 115,
                'description': 'dynamic, surprising & experimental beats'
            },
            'Disgust': {
                'target_valence': 0.50,
                'target_energy': 0.45,
                'target_tempo': 90,
                'description': 'refreshing acoustic & chill synth tracks'
            },
            'Neutral': {
                'target_valence': 0.55,
                'target_energy': 0.50,
                'target_tempo': 95,
                'description': 'balanced and versatile acoustic tracks'
            }
        }

        # ─────────────────────────────────────────────────────────────────────
        # EMOTION TRACK DATABASE
        # Each track has a 'local_file' field — the filename you drop into
        #   static/music/
        # The app auto-checks if that file exists; if yes it uses it for
        # playback. Otherwise it falls back to the 'url' (online preview).
        # ─────────────────────────────────────────────────────────────────────
        self.EMOTION_TRACKS = {
            # ── HAPPY ── local: Egire-Mabbulalona.mp3
            'Happy': [
                {'name': 'Egirey Mabbulona',    'artist': 'Sid Sriram',              'local_file': 'Egire-Mabbulalona.mp3',       'youtube_id': 'bWXazVhlyxQ', 'embed_url': 'https://www.youtube.com/embed/bWXazVhlyxQ', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',  'spotify_url': 'https://open.spotify.com/search/Egirey%20Mabbulona'},
                {'name': 'Butta Bomma',         'artist': 'Armaan Malik',            'local_file': 'Egire-Mabbulalona.mp3',       'youtube_id': '2mDCVzruYzQ', 'embed_url': 'https://www.youtube.com/embed/2mDCVzruYzQ', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',  'spotify_url': 'https://open.spotify.com/search/Butta%20Bomma'},
            ],
            # ── SAD ── local: stream.mp3 (used as fallback sad song)
            'Sad': [
                {'name': 'Nee Gunde Lona',          'artist': 'Sid Sriram',          'local_file': 'stream.mp3',                  'youtube_id': '5qap5aO4i9A', 'embed_url': 'https://www.youtube.com/embed/5qap5aO4i9A', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3',  'spotify_url': 'https://open.spotify.com/search/Nee%20Gunde%20Lona'},
                {'name': 'Nee Kannu Neeli Samudram','artist': 'Javed Ali',           'local_file': 'stream.mp3',                  'youtube_id': 'mL3V4v2c4c4', 'embed_url': 'https://www.youtube.com/embed/mL3V4v2c4c4', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3',  'spotify_url': 'https://open.spotify.com/search/Nee%20Kannu%20Neeli%20Samudram'},
            ],
            # ── ANGRY ── local: Karuppa-Kooda-Va-Lyric-Video-Karuppu-Suriya-RJ-Balaji-@SaiAbhyankkar-VM-Mahalingam.mp3
            'Angry': [
                {'name': 'Karuppa Kooda Va',  'artist': 'Sai Abhyankkar',            'local_file': 'Karuppa-Kooda-Va-Lyric-Video-Karuppu-Suriya-RJ-Balaji-@SaiAbhyankkar-VM-Mahalingam.mp3', 'youtube_id': '9kpygZ_k6cM', 'embed_url': 'https://www.youtube.com/embed/9kpygZ_k6cM', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3', 'spotify_url': 'https://open.spotify.com/search/Karuppa%20Kooda%20Va'},
                {'name': 'Raa Raa',           'artist': 'Devi Sri Prasad',           'local_file': 'Karuppa-Kooda-Va-Lyric-Video-Karuppu-Suriya-RJ-Balaji-@SaiAbhyankkar-VM-Mahalingam.mp3', 'youtube_id': 'bWXazVhlyxQ', 'embed_url': 'https://www.youtube.com/embed/bWXazVhlyxQ', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3', 'spotify_url': 'https://open.spotify.com/search/Raa%20Raa'},
            ],
            # ── FEAR ── local: Fire-Song-Tamil-Lyrical-Kanguva-Suriya-Devi-Sri-Prasad-Siva-Viveka.mp3
            'Fear': [
                {'name': 'Fire Song',        'artist': 'Devi Sri Prasad',            'local_file': 'Fire-Song-Tamil-Lyrical-Kanguva-Suriya-Devi-Sri-Prasad-Siva-Viveka.mp3', 'youtube_id': 'bWXazVhlyxQ', 'embed_url': 'https://www.youtube.com/embed/bWXazVhlyxQ', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',  'spotify_url': 'https://open.spotify.com/search/Fire%20Song'},
                {'name': 'Gundello Emundo',  'artist': 'Sid Sriram',                 'local_file': 'Fire-Song-Tamil-Lyrical-Kanguva-Suriya-Devi-Sri-Prasad-Siva-Viveka.mp3', 'youtube_id': '5qap5aO4i9A', 'embed_url': 'https://www.youtube.com/embed/5qap5aO4i9A', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3',  'spotify_url': 'https://open.spotify.com/search/Gundello%20Emundo'},
            ],
            # ── SURPRISE ── local: Almost-Padipoyindhe-Pilla-Lyrical-Das-Ka-Dhamki-Vishwaksen-Nivetha-Pethuraj-Leon-James.mp3
            'Surprise': [
                {'name': 'Almost Padipoyindhe Pilla', 'artist': 'Leon James',        'local_file': 'Almost-Padipoyindhe-Pilla-Lyrical-Das-Ka-Dhamki-Vishwaksen-Nivetha-Pethuraj-Leon-James.mp3', 'youtube_id': '2mDCVzruYzQ', 'embed_url': 'https://www.youtube.com/embed/2mDCVzruYzQ', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3', 'spotify_url': 'https://open.spotify.com/search/Almost%20Padipoyindhe%20Pilla'},
                {'name': 'Naatu Naatu',              'artist': 'Rahul Sipligunj',     'local_file': 'Almost-Padipoyindhe-Pilla-Lyrical-Das-Ka-Dhamki-Vishwaksen-Nivetha-Pethuraj-Leon-James.mp3', 'youtube_id': 's8Y2E8j6h9k', 'embed_url': 'https://www.youtube.com/embed/s8Y2E8j6h9k', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3', 'spotify_url': 'https://open.spotify.com/search/Naatu%20Naatu'},
            ],
            # ── DISGUST ── local: stream.mp3
            'Disgust': [
                {'name': 'Oh Baby',      'artist': 'Mickey J Meyer',  'local_file': 'stream.mp3', 'youtube_id': 'eQI5u13wX30', 'embed_url': 'https://www.youtube.com/embed/eQI5u13wX30', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3', 'spotify_url': 'https://open.spotify.com/search/Oh%20Baby'},
            ],
            # ── NEUTRAL ── local: Peniviti - SenSongsMp3.Co.mp3
            'Neutral': [
                {'name': 'Peniviti',       'artist': 'Kaala Bhairava', 'local_file': 'Peniviti - SenSongsMp3.Co.mp3', 'youtube_id': '5qap5aO4i9A', 'embed_url': 'https://www.youtube.com/embed/5qap5aO4i9A', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3', 'spotify_url': 'https://open.spotify.com/search/Peniviti'},
                {'name': 'Maate Vinadhuga','artist': 'Sid Sriram',     'local_file': 'Peniviti - SenSongsMp3.Co.mp3', 'youtube_id': 'mL3V4v2c4c4', 'embed_url': 'https://www.youtube.com/embed/mL3V4v2c4c4', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',  'spotify_url': 'https://open.spotify.com/search/Maate%20Vinadhuga'},
            ],
        }
        # Path to the local music folder (relative to the project root)
        self.music_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'music')

    def connect_spotify(self):
        """Initialize Spotify API connection if credentials exist"""
        try:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            
            if client_id and client_secret and client_id != 'your_client_id_here':
                auth_manager = SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
                print("[OK] Spotify API connected successfully")
                return True
            else:
                print("[NOTICE] Spotify credentials not configured. Using Licensed Track Database.")
                return False
        except Exception as e:
            print(f"[NOTICE] Error connecting to Spotify: {e}")
            return False

    def get_recommendations(self, emotion, limit=10, music_intent=None):
        """
        Get music recommendations based on detected emotion & LLM music intent.
        Returns curated Telugu & licensed track recommendations with audio preview & video embed URLs.
        If a matching local MP3 exists in static/music/, that file is used for playback.
        """
        if emotion not in self.emotion_to_music_params:
            emotion = 'Neutral'

        # Try Spotify API first if connected
        if self.sp:
            try:
                query = f"telugu {emotion.lower()} song"
                results = self.sp.search(q=query, type='track', market='IN', limit=limit*2)
                tracks = []
                for track in results['tracks']['items']:
                    tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'] if track['artists'] else 'Telugu Artist',
                        'album': track['album']['name'] if track.get('album') else '',
                        'preview_url': track.get('preview_url') or 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                        'spotify_url': track['external_urls']['spotify'] if track.get('external_urls') else None,
                        'url': track.get('preview_url') or 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
                    })
                    if len(tracks) >= limit:
                        break
                if tracks:
                    return tracks
            except Exception as e:
                print(f"[NOTICE] Spotify fetch fallback: {e}")

        # EMOTION_TRACKS database — auto-resolve local MP3 if present in static/music/
        raw_tracks = self.EMOTION_TRACKS.get(emotion, self.EMOTION_TRACKS['Neutral'])
        res_tracks = [self._resolve_track_url(t) for t in list(raw_tracks)]

        # Supplement up to `limit` from Neutral if needed
        if len(res_tracks) < limit:
            extra = [self._resolve_track_url(t)
                     for t in self.EMOTION_TRACKS['Neutral']
                     if t not in raw_tracks]
            res_tracks.extend(extra)

        return res_tracks[:limit]

    def _resolve_track_url(self, track):
        """
        Returns a copy of the track dict with `url` set to the local MP3 path
        if a matching file exists on disk. Checks (in priority order):
          1. static/music/<local_file>           (flat — current layout)
          2. static/music/<emotion>/<local_file> (subfolder — future layout)
        Falls back to online url if neither exists.
        """
        t = dict(track)  # copy so we don't mutate the original
        local_file = t.get('local_file')
        emotion    = t.get('emotion', '')

        if local_file:
            # 1. Flat path
            flat_path = os.path.join(self.music_folder, local_file)
            if os.path.isfile(flat_path):
                t['url']    = f'/static/music/{local_file}'
                t['source'] = 'local'
                return t

            # 2. Emotion subfolder path  e.g. static/music/happy/Egire-Mabbulalona.mp3
            if emotion:
                sub_folder = emotion.lower()
                sub_path   = os.path.join(self.music_folder, sub_folder, local_file)
                if os.path.isfile(sub_path):
                    t['url']    = f'/static/music/{sub_folder}/{local_file}'
                    t['source'] = 'local'
                    return t

        t['source'] = 'online'
        return t


# Create global instance
music_recommender = MusicRecommender()
