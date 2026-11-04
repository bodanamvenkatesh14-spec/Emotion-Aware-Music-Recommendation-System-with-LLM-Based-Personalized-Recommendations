/**
 * EmotionAI - Multi-Modal Emotion Music System Frontend Script
 * Includes LLM Service Layer, Music Intent Display & Interactive AI Chat Assistant
 */

// Global App State
const state = {
    currentMode: 'camera',   // 'camera' | 'text'
    videoStream: null,
    currentEmotion: 'Neutral',
    previousEmotion: null,      // for mood shift detection
    faceEmotion: 'Neutral',
    faceConfidence: 0.80,
    textEmotion: 'Neutral',
    textConfidence: 0.65,
    overallConfidence: 0.74,
    playlist: [],
    currentTrackIndex: 0,
    isPlaying: false,
    shuffleOn: false,
    repeatOn: false,
    userId: null,
    username: null
};

// Map of Emotion metadata
const EMOTION_META = {
    'Happy':   { emoji: '😊', playlist: 'Happy Vibe Playlist',    genre: 'Upbeat & Feel-Good Telugu Beats',   color: '#ffb703' },
    'Sad':     { emoji: '😢', playlist: 'Melancholy Melodies',     genre: 'Soothing Melodies & Acoustic',      color: '#3a7bd5' },
    'Angry':   { emoji: '😡', playlist: 'Angry Playlist',          genre: 'High Energy - Intense Beats',       color: '#ff0055' },
    'Fear':    { emoji: '😨', playlist: 'Calming Essentials',      genre: 'Ambient & Deep Relaxation',         color: '#764ba2' },
    'Surprise':{ emoji: '😲', playlist: 'Surprise Hits',           genre: 'Experimental & Dynamic Tracks',     color: '#00f2fe' },
    'Disgust': { emoji: '🤢', playlist: 'Mind Detox',              genre: 'Fresh Instrumental & Chill Synth',  color: '#2ecc71' },
    'Neutral': { emoji: '😐', playlist: 'Focus & Chill',           genre: 'Lo-Fi Beats & Ambient Soundscapes', color: '#95a5a6' }
};

// Default suggestions for instant playback
const DEFAULT_SUGGESTIONS = [
    { name: 'Egirey Mabbulona', artist: 'Sid Sriram', url: '/static/music/Egire-Mabbulalona.mp3' },
    { name: 'Peniviti',          artist: 'Kaala Bhairava', url: '/static/music/Peniviti - SenSongsMp3.Co.mp3' },
    { name: 'Almost Padipoyindhe Pilla', artist: 'Leon James', url: '/static/music/Almost-Padipoyindhe-Pilla-Lyrical-Das-Ka-Dhamki-Vishwaksen-Nivetha-Pethuraj-Leon-James.mp3' }
];

document.addEventListener('DOMContentLoaded', () => {
    initializeModeButtons();
    initializeCamera();        // start camera by default (camera mode is first)
    initializeEventListeners();
    initializeAudioPlayer();
    initializeAuthAndDashboard();
    initializeChatAssistant();
    loadSuggestedTracks(DEFAULT_SUGGESTIONS);
});

// ── Mode Switching (Camera ↔ Text) ───────────────────────────────────────────
function initializeModeButtons() {
    const cameraBtn  = document.getElementById('cameraModeBtn');
    const textBtn    = document.getElementById('textModeBtn');
    const cameraSection = document.getElementById('cameraModeSection');
    const textSection   = document.getElementById('textModeSection');

    function switchToCamera() {
        state.currentMode = 'camera';
        cameraBtn.classList.add('active');
        textBtn.classList.remove('active');
        cameraSection.classList.remove('hidden');
        textSection.classList.add('hidden');
        initializeCamera();   // ensure camera stream is on
    }

    function switchToText() {
        state.currentMode = 'text';
        textBtn.classList.add('active');
        cameraBtn.classList.remove('active');
        textSection.classList.remove('hidden');
        cameraSection.classList.add('hidden');
        // Stop camera stream to save resources
        if (state.videoStream) {
            state.videoStream.getTracks().forEach(t => t.stop());
            state.videoStream = null;
        }
    }

    if (cameraBtn) cameraBtn.addEventListener('click', switchToCamera);
    if (textBtn)   textBtn.addEventListener('click', switchToText);
}

// ── Camera Setup ─────────────────────────────────────────────────────────────
async function initializeCamera() {
    const video = document.getElementById('videoElement');
    if (!video) return;
    if (state.videoStream) return;  // already running

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 1280 }, height: { ideal: 720 } }
        });
        state.videoStream = stream;
        video.srcObject = stream;
    } catch (err) {
        console.warn('Camera access issue:', err);
    }
}

function captureImage() {
    const video  = document.getElementById('videoElement');
    const canvas = document.getElementById('canvasElement');
    if (!video || !canvas) return null;
    canvas.width  = video.videoWidth  || 640;
    canvas.height = video.videoHeight || 480;
    canvas.getContext('2d').drawImage(video, 0, 0);
    return canvas.toDataURL('image/jpeg');
}

// ── Event Listeners ───────────────────────────────────────────────────────────
function initializeEventListeners() {
    // Camera Mode analyse button
    const cameraBtn = document.getElementById('analyzeCameraBtn');
    if (cameraBtn) cameraBtn.addEventListener('click', runCameraAnalysis);

    // Text Mode analyse button
    const textBtn = document.getElementById('analyzeTextBtn');
    if (textBtn) textBtn.addEventListener('click', runTextAnalysis);

    // Emotion Badge manual override clicks (middle column)
    document.querySelectorAll('.emotion-badge-item').forEach(item => {
        item.addEventListener('click', () => {
            const emotion = item.dataset.emotion;
            if (emotion) {
                updateEmotionDisplay(emotion, emotion, 'Manual Selection', 0.95);
                fetchLLMAnalysis(emotion, 0.95, emotion, 0.90);
                fetchMusicRecommendations(emotion);

            }
        });
    });
}

// ── Camera Mode Analysis ──────────────────────────────────────────────────────
async function runCameraAnalysis() {
    showStatus('Capturing face emotion...', 'success');
    const imageData = captureImage();
    if (!imageData) {
        showStatus('Camera not ready. Please allow camera access.', 'error');
        return;
    }

    const payload = { image: imageData };
    if (state.userId) payload.user_id = state.userId;

    try {
        const response = await fetch('/api/detect-emotion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (result.success) {
            const emotion = result.emotion || 'Neutral';
            const conf    = result.confidence || 0.80;
            state.faceEmotion    = emotion;
            state.faceConfidence = conf;
            state.currentEmotion = emotion;
            state.overallConfidence = conf;

            // ✅ This highlights the correct badge with glow + DETECTED label
            updateEmotionDisplay(emotion, emotion, '', conf);

            fetchLLMAnalysis(emotion, conf, emotion, conf);
            if (result.recommendations?.length) loadSuggestedTracks(result.recommendations);
            else fetchMusicRecommendations(emotion);
            showStatus('Face emotion detected: ' + emotion, 'success');
        } else {
            showStatus(result.message || 'No face detected — try again', 'error');
        }
    } catch (err) {
        console.error('Camera analysis error:', err);
        showStatus('Camera analysis failed. Try again.', 'error');
    }
}

// ── Text Mode Analysis ────────────────────────────────────────────────────────
async function runTextAnalysis() {
    const textInput = (document.getElementById('emotionText')?.value || '').trim();
    if (!textInput) {
        showStatus('Please type something first!', 'error');
        return;
    }
    showStatus('Analysing text sentiment...', 'success');

    const payload = { text: textInput };
    if (state.userId) payload.user_id = state.userId;

    try {
        const response = await fetch('/api/analyze-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (result.success) {
            const emotion = result.emotion || 'Neutral';
            const conf    = result.confidence || 0.75;
            state.textEmotion    = emotion;
            state.textConfidence = conf;
            state.currentEmotion = emotion;
            state.overallConfidence = conf;

            const snippet = '"' + textInput.slice(0, 30) + (textInput.length > 30 ? '...' : '') + '"';

            // ✅ Highlights the correct badge with glow + DETECTED label
            updateEmotionDisplay(emotion, emotion, snippet, conf);

            fetchLLMAnalysis(emotion, conf, emotion, conf);
            if (result.recommendations?.length) loadSuggestedTracks(result.recommendations);
            else fetchMusicRecommendations(emotion);
            showStatus('Mood detected from text: ' + emotion, 'success');
        } else {
            showStatus(result.message || 'Text analysis failed', 'error');
        }
    } catch (err) {
        console.error('Text analysis error:', err);
        showStatus('Text analysis failed. Try again.', 'error');
    }
}


// Fetch LLM Analysis (Explanation & Music Intent)
async function fetchLLMAnalysis(faceEmo, faceConf, textEmo, textConf) {
    const payload = {
        face_emotion: faceEmo,
        face_confidence: faceConf,
        text_emotion: textEmo,
        text_confidence: textConf,
        overall_emotion: state.currentEmotion,
        overall_confidence: state.overallConfidence
    };

    try {
        const response = await fetch('/api/llm/emotion-analysis', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (data.success) {
            updateLLMInsightCard(data.explanation, data.suggestion, data.music_intent);
        }
    } catch (err) {
        console.warn('LLM fetch error:', err);
    }
}

// Update LLM Insight Card in Middle Column
function updateLLMInsightCard(explanation, suggestion, intent) {
    const expEl = document.getElementById('llmExplanationText');
    const sugEl = document.getElementById('llmSuggestionText');
    const energyEl = document.getElementById('intentEnergyVal');
    const valenceEl = document.getElementById('intentValenceVal');
    const tempoEl = document.getElementById('intentTempoVal');

    if (expEl && explanation) expEl.textContent = explanation;
    if (sugEl && suggestion) sugEl.innerHTML = `💡 <em>${suggestion}</em>`;
    
    if (intent) {
        if (energyEl) energyEl.textContent = `${Math.round((intent.energy || 0.8) * 100)}%`;
        if (valenceEl) valenceEl.textContent = `${Math.round((intent.valence || 0.7) * 100)}%`;
        if (tempoEl) tempoEl.textContent = `${intent.tempo || 120} BPM`;
    }
}

// Update UI Components across 3 columns
function updateEmotionDisplay(overallEmotion, faceEmotion, textSnippet, confidence) {
    // ── Mood Shift Detection ─────────────────────────────────────────────────
    const prev = state.previousEmotion;
    if (prev && prev !== overallEmotion) {
        const prevMeta = EMOTION_META[prev]  || { emoji: '😐' };
        const currMeta = EMOTION_META[overallEmotion] || { emoji: '😐' };
        const banner = document.getElementById('moodShiftBanner');
        const detail = document.getElementById('moodShiftDetail');
        if (banner && detail) {
            detail.textContent = prevMeta.emoji + ' ' + prev + ' → ' + currMeta.emoji + ' ' + overallEmotion;
            banner.classList.remove('hidden');
            // Auto-hide after 6 seconds
            clearTimeout(banner._hideTimer);
            banner._hideTimer = setTimeout(() => banner.classList.add('hidden'), 6000);
        }
    }
    state.previousEmotion = overallEmotion;
    state.currentEmotion  = overallEmotion;
    const meta = EMOTION_META[overallEmotion] || EMOTION_META['Neutral'];

    // Left Column Pill Updates
    const faceEl    = document.getElementById('faceEmotionResult');
    const textEl    = document.getElementById('textSnippetResult');
    const overallEl = document.getElementById('overallEmotionResult');
    const overallTextEl = document.getElementById('overallEmotionResultText');

    const fConfPct = Math.round((state.faceConfidence || 0.8) * 100);
    const oConfPct = Math.round((confidence || 0.88) * 100);

    if (faceEl)       faceEl.innerHTML    = `${meta.emoji} ${faceEmotion || overallEmotion} (${fConfPct}%)`;
    if (textEl && textSnippet) textEl.textContent = textSnippet;
    if (overallEl)    overallEl.innerHTML = `${meta.emoji} ${overallEmotion} (${oConfPct}%)`;
    if (overallTextEl) overallTextEl.innerHTML = `${meta.emoji} ${overallEmotion} (${oConfPct}%)`;

    // Middle Column Badges — highlight detected emotion
    document.querySelectorAll('.emotion-badge-item').forEach(item => {
        item.classList.remove('active');
        const tag = item.querySelector('.detected-tag');
        if (tag) tag.remove();

        if (item.dataset.emotion === overallEmotion) {
            item.classList.add('active');
            const newTag = document.createElement('span');
            newTag.className = 'detected-tag';
            newTag.textContent = 'Detected';
            item.appendChild(newTag);
        }
    });

    // Middle Column Playlist titles
    const titleEl = document.getElementById('playlistCategoryTitle');
    const subEl   = document.getElementById('playlistGenreSubtitle');
    if (titleEl) titleEl.textContent = meta.playlist;
    if (subEl)   subEl.textContent   = meta.genre;
}

// Fetch Recommendations from API
async function fetchMusicRecommendations(emotion) {
    try {
        const response = await fetch('/api/recommend-music', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emotion, limit: 5 })
        });
        const data = await response.json();
        if (data.success && data.recommendations) {
            loadSuggestedTracks(data.recommendations);
        }
    } catch (err) {
        console.warn('Music fetch error:', err);
    }
}

// Load Suggested Tracks into Right Column
function loadSuggestedTracks(tracks) {
    const listEl = document.getElementById('suggestedTracksList');
    if (!listEl) return;

    listEl.innerHTML = '';
    state.playlist = tracks;

    tracks.forEach((track, index) => {
        const li = document.createElement('li');
        li.className = `track-item ${index === 0 ? 'active' : ''}`;
        li.innerHTML = `<span class="bullet">•</span> ${track.artist || 'Artist'} - ${track.name || track.title || 'Track'}`;
        
        li.addEventListener('click', () => {
            document.querySelectorAll('.track-item').forEach(el => el.classList.remove('active'));
            li.classList.add('active');
            playTrack(index);
        });

        listEl.appendChild(li);
    });

    if (tracks.length > 0) {
        playTrack(0, false);
    }
}

// Audio Player Deck Logic
function initializeAudioPlayer() {
    const audio = document.getElementById('audioPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playPauseIcon = document.getElementById('playPauseIcon');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const shuffleBtn = document.getElementById('shuffleBtn');
    const repeatBtn = document.getElementById('repeatBtn');
    const volumeSlider = document.getElementById('volumeSlider');
    const progressBarContainer = document.getElementById('progressBarContainer');

    if (!audio) return;

    // Play / Pause
    playPauseBtn.addEventListener('click', () => {
        if (state.isPlaying) {
            audio.pause();
            state.isPlaying = false;
            if (playPauseIcon) playPauseIcon.textContent = '▶';
        } else {
            audio.play().then(() => {
                state.isPlaying = true;
                if (playPauseIcon) playPauseIcon.textContent = '⏸';
            }).catch(() => {
                state.isPlaying = true;
                if (playPauseIcon) playPauseIcon.textContent = '⏸';
            });
        }
    });

    // Prev / Next
    if (prevBtn) prevBtn.addEventListener('click', () => playTrack(Math.max(0, state.currentTrackIndex - 1)));
    if (nextBtn) nextBtn.addEventListener('click', () => playTrack(Math.min(state.playlist.length - 1, state.currentTrackIndex + 1)));

    // Shuffle toggle
    if (shuffleBtn) {
        shuffleBtn.addEventListener('click', () => {
            state.shuffleOn = !state.shuffleOn;
            shuffleBtn.classList.toggle('active', state.shuffleOn);
        });
    }

    // Repeat toggle
    if (repeatBtn) {
        repeatBtn.addEventListener('click', () => {
            state.repeatOn = !state.repeatOn;
            repeatBtn.classList.toggle('active', state.repeatOn);
            audio.loop = state.repeatOn;
        });
    }

    // Volume
    if (volumeSlider) {
        volumeSlider.addEventListener('input', (e) => {
            audio.volume = e.target.value / 100;
        });
    }

    // Click on progress bar to seek
    if (progressBarContainer) {
        progressBarContainer.addEventListener('click', (e) => {
            const rect = progressBarContainer.getBoundingClientRect();
            const pos = (e.clientX - rect.left) / rect.width;
            if (audio.duration) audio.currentTime = pos * audio.duration;
        });
    }

    // Time update — drive pink progress bar + thumb
    audio.addEventListener('timeupdate', () => {
        const curTimeEl = document.getElementById('currentTime');
        const totTimeEl = document.getElementById('totalTime');
        const progressFill = document.getElementById('progressBar');
        const progressThumb = document.getElementById('progressThumb');

        if (audio.duration) {
            const pct = (audio.currentTime / audio.duration) * 100;
            if (progressFill) progressFill.style.width = `${pct}%`;
            if (progressThumb) progressThumb.style.left = `${pct}%`;
            if (curTimeEl) curTimeEl.textContent = formatTime(audio.currentTime);
            if (totTimeEl) totTimeEl.textContent = formatTime(audio.duration);
        }
    });

    // Auto-next when track ends
    audio.addEventListener('ended', () => {
        state.isPlaying = false;
        if (playPauseIcon) playPauseIcon.textContent = '▶';
        if (state.shuffleOn && state.playlist.length > 1) {
            let next = state.currentTrackIndex;
            while (next === state.currentTrackIndex) {
                next = Math.floor(Math.random() * state.playlist.length);
            }
            playTrack(next);
        } else if (state.currentTrackIndex < state.playlist.length - 1) {
            playTrack(state.currentTrackIndex + 1);
        }
    });
}

function playTrack(index, autoStart = true) {
    if (!state.playlist[index]) return;
    state.currentTrackIndex = index;
    const track = state.playlist[index];

    // IDs
    const titleEl = document.getElementById('playerTrackName');
    const artistEl = document.getElementById('playerArtistName');
    const albumArt = document.getElementById('albumArtImg');
    const videoThumb = document.getElementById('videoPlayerThumbnail');
    const youtubeIframe = document.getElementById('youtubeIframe');
    const audio = document.getElementById('audioPlayer');
    const npDescEl = document.getElementById('npTrackDesc');
    const npEmotionPill = document.getElementById('npEmotionPill');
    const npEmotionEmoji = document.getElementById('npEmotionEmoji');

    const trackTitle = track.name || track.title || 'Now Playing';
    const trackArtist = track.artist || '';
    const meta = EMOTION_META[state.currentEmotion] || EMOTION_META['Neutral'];

    if (titleEl) titleEl.textContent = trackTitle;
    if (artistEl) artistEl.textContent = trackArtist;

    // Album Art — use YouTube thumbnail if available, else a gradient placeholder
    const ytid = track.youtube_id || 'bWXazVhlyxQ';
    const artSrc = `https://img.youtube.com/vi/${ytid}/mqdefault.jpg`;
    if (albumArt) albumArt.src = artSrc;
    if (videoThumb) videoThumb.src = `https://img.youtube.com/vi/${ytid}/maxresdefault.jpg`;

    // YouTube iframe embed
    if (youtubeIframe && autoStart && track.embed_url) {
        youtubeIframe.src = `${track.embed_url}?autoplay=1`;
    }

    // Emotion pill update
    if (npEmotionEmoji) npEmotionEmoji.textContent = meta.emoji || '🙂';
    if (npEmotionPill) npEmotionPill.textContent = `Emotion: ${state.currentEmotion}`;

    // Track description from LLM insight or genre
    if (npDescEl) {
        npDescEl.textContent = document.getElementById('llmExplanationText')?.textContent
            || `${meta.genre} — matching your current ${state.currentEmotion.toLowerCase()} mood.`;
    }

    // Audio playback
    if (audio && (track.preview_url || track.url)) {
        audio.src = track.preview_url || track.url;
        if (autoStart) {
            audio.play().then(() => {
                state.isPlaying = true;
                const icon = document.getElementById('playPauseIcon');
                if (icon) icon.textContent = '⏸';
            }).catch(err => console.log('Autoplay prevented:', err));
        }
    }

    // Mark active in track list
    document.querySelectorAll('.track-item').forEach((el, i) => {
        el.classList.toggle('active', i === index);
    });
}


function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
}

// 🤖 Interactive AI Chat Assistant Logic
function initializeChatAssistant() {
    const sendBtn = document.getElementById('sendChatBtn');
    const input = document.getElementById('chatInput');
    const container = document.getElementById('chatMessagesContainer');
    const clearBtn = document.getElementById('clearChatBtn');
    const chips = document.querySelectorAll('.chip-btn');

    if (!sendBtn || !input || !container) return;

    const sendMessage = async (msgText) => {
        const text = msgText || input.value.trim();
        if (!text) return;

        // Append User Bubble
        appendChatBubble('user', text);
        if (!msgText) input.value = '';

        // Typing Indicator Bubble
        const typingBubble = appendChatBubble('bot', '🤖 <em>EmotionAI is thinking...</em>');

        try {
            const context = {
                overall_emotion: state.currentEmotion,
                face_emotion: state.faceEmotion,
                text_emotion: state.textEmotion,
                current_track: `${document.getElementById('playerTrackName').textContent} - ${document.getElementById('playerArtistName').textContent}`
            };

            const response = await fetch('/api/llm/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    user_id: state.userId,
                    context: context
                })
            });

            const data = await response.json();
            typingBubble.remove();

            if (data.success && data.response) {
                appendChatBubble('bot', data.response);
            } else {
                appendChatBubble('bot', "I'm currently tuning into your mood! Feel free to ask about Telugu recommendations.");
            }
        } catch (err) {
            typingBubble.remove();
            appendChatBubble('bot', `Currently playing music for your **${state.currentEmotion}** vibe!`);
        }
    };

    sendBtn.addEventListener('click', () => sendMessage());
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const question = chip.dataset.question || chip.textContent;
            sendMessage(question);
        });
    });

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            container.innerHTML = `
                <div class="chat-bubble bot">
                    <span class="bubble-sender">🤖 EmotionAI Assistant</span>
                    <p>Chat cleared! How can I assist you with your music or mood today?</p>
                </div>
            `;
        });
    }
}

function appendChatBubble(role, text) {
    const container = document.getElementById('chatMessagesContainer');
    if (!container) return null;

    const div = document.createElement('div');
    div.className = `chat-bubble ${role}`;
    const sender = role === 'user' ? '👤 You' : '🤖 EmotionAI';
    div.innerHTML = `<span class="bubble-sender">${sender}</span><p>${text}</p>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
}

// User Auth & Dashboard Modals
function initializeAuthAndDashboard() {
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const submitLoginBtn = document.getElementById('submitLoginBtn');
    const closeLoginBtn = document.getElementById('closeLoginBtn');
    const usernameInput = document.getElementById('usernameInput');
    const userNameText = document.getElementById('userNameText');
    const dashboardBtn = document.getElementById('dashboardBtn');
    const dashboardSection = document.getElementById('dashboardSection');
    const closeDashboardBtn = document.getElementById('closeDashboardBtn');

    if (loginBtn && loginModal) {
        loginBtn.addEventListener('click', () => loginModal.classList.remove('hidden'));
        closeLoginBtn.addEventListener('click', () => loginModal.classList.add('hidden'));

        submitLoginBtn.addEventListener('click', async () => {
            const name = usernameInput.value.trim();
            if (!name) return;

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: name })
                });
                const data = await res.json();
                if (data.success) {
                    state.userId = data.user_id;
                    state.username = data.username;
                    userNameText.textContent = `Hello, ${data.username}!`;
                    loginModal.classList.add('hidden');
                    loginBtn.classList.add('hidden');
                    dashboardBtn.classList.remove('hidden');
                    showStatus(`Welcome, ${data.username}!`, 'success');
                }
            } catch (err) {
                userNameText.textContent = `Hello, ${name}!`;
                loginModal.classList.add('hidden');
            }
        });
    }

    if (dashboardBtn && dashboardSection) {
        dashboardBtn.addEventListener('click', async () => {
            dashboardSection.classList.remove('hidden');
            if (state.userId) {
                try {
                    const res = await fetch(`/api/llm/daily-summary?user_id=${state.userId}`);
                    const data = await res.json();
                    if (data.success && data.llm_insight) {
                        const insightEl = document.getElementById('llmDailyInsightText');
                        if (insightEl) insightEl.textContent = `AI Insight: ${data.llm_insight}`;
                    }
                } catch(e) {}
            }
        });
        closeDashboardBtn.addEventListener('click', () => dashboardSection.classList.add('hidden'));
    }
}

// Status Toast
function showStatus(msg, type = 'success') {
    const el = document.getElementById('statusMessage');
    if (!el) return;
    el.textContent = msg;
    el.className = `status-message show ${type}`;
    setTimeout(() => el.classList.remove('show'), 4000);
}
