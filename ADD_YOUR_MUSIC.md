# 🎵 Add Your Own Music - Easy Guide

## How to Add Your Favorite Songs

### Step 1: Choose Your Songs
Decide which songs you want for each emotion:
- 😊 **Happy** - Upbeat, energetic songs
- 😢 **Sad** - Calm, emotional songs  
- 😠 **Angry** - Intense, powerful songs
- 😨 **Fear** - Relaxing, calming songs
- 😲 **Surprise** - Interesting, dynamic songs
- 🤢 **Disgust** - Alternative, thoughtful songs
- 😐 **Neutral** - Balanced, versatile songs

### Step 2: Format Your Songs
Each song needs 3 pieces of information:
1. **name** - Song title and artist (e.g., "Shape of You - Ed Sheeran")
2. **artist** - Artist name (e.g., "Ed Sheeran")
3. **genre** - Music genre (e.g., "Pop")

### Step 3: Add to the File

Open: `models/music_recommender.py`

Find the section starting at line 69: `self.fallback_recommendations = {`

---

## 📝 Template: Copy & Paste This Format

```python
'Happy': [
    {'name': 'YOUR_SONG_NAME', 'artist': 'YOUR_ARTIST', 'genre': 'GENRE'},
    # Add more songs here...
],
```

---

## 🎯 Example: Adding Your Own Songs

### Example 1: Add Bollywood Songs

```python
'Happy': [
    {'name': 'Badtameez Dil', 'artist': 'Benny Dayal', 'genre': 'Bollywood'},
    {'name': 'Gallan Goodiyaan', 'artist': 'Various Artists', 'genre': 'Bollywood'},
    {'name': 'Chammak Challo', 'artist': 'Akon', 'genre': 'Bollywood'},
    {'name': 'Sooraj Dooba Hain', 'artist': 'Arijit Singh', 'genre': 'Bollywood'},
],
```

### Example 2: Add K-Pop Songs

```python
'Happy': [
    {'name': 'Dynamite - BTS', 'artist': 'BTS', 'genre': 'K-Pop'},
    {'name': 'How You Like That - BLACKPINK', 'artist': 'BLACKPINK', 'genre': 'K-Pop'},
    {'name': 'Gangnam Style - PSY', 'artist': 'PSY', 'genre': 'K-Pop'},
],
```

### Example 3: Add Your Playlist

```python
'Neutral': [
    {'name': 'Your Favorite Song 1', 'artist': 'Your Artist 1', 'genre': 'Rock'},
    {'name': 'Your Favorite Song 2', 'artist': 'Your Artist 2', 'genre': 'Pop'},
    {'name': 'Your Favorite Song 3', 'artist': 'Your Artist 3', 'genre': 'Hip-Hop'},
],
```

---

## 🚀 Quick Edit Instructions

### Option 1: Tell Me Your Songs
Just tell me:
- Which emotion category (Happy, Sad, Angry, etc.)
- List of songs you want

**Example:**
```
For Happy, add:
1. Shape of You - Ed Sheeran
2. Senorita - Shawn Mendes
3. Dance Monkey - Tones and I

For Sad, add:
1. Someone You Loved - Lewis Capaldi
2. Perfect - Ed Sheeran
```

### Option 2: I'll Edit the File for You
Tell me:
1. Emotion category
2. Songs with artists
And I'll add them automatically!

---

## 📋 Template for Each Emotion

Copy this and fill in your songs:

```python
self.fallback_recommendations = {
    'Happy': [
        {'name': 'Song 1 Title', 'artist': 'Artist 1', 'genre': 'Pop'},
        {'name': 'Song 2 Title', 'artist': 'Artist 2', 'genre': 'Pop'},
        {'name': 'Song 3 Title', 'artist': 'Artist 3', 'genre': 'Rock'},
        {'name': 'Song 4 Title', 'artist': 'Artist 4', 'genre': 'EDM'},
        # Add as many as you want!
    ],
    
    'Sad': [
        {'name': 'Song Title', 'artist': 'Artist', 'genre': 'Ballad'},
        # Your sad songs here...
    ],
    
    'Angry': [
        {'name': 'Song Title', 'artist': 'Artist', 'genre': 'Metal'},
        # Your angry songs here...
    ],
    
    'Fear': [
        {'name': 'Song Title', 'artist': 'Artist', 'genre': 'Ambient'},
        # Your calming songs here...
    ],
    
    'Surprise': [
        {'name': 'Song Title', 'artist': 'Artist', 'genre': 'Electronic'},
        # Your surprise songs here...
    ],
    
    'Disgust': [
        {'name': 'Song Title', 'artist': 'Artist', 'genre': 'Alternative'},
        # Your songs here...
    ],
    
    'Neutral': [
        {'name': 'Song Title', 'artist': 'Artist', 'genre': 'Rock'},
        # Your neutral songs here...
    ]
}
```

---

## ⚠️ Important Rules

1. **Use Single Quotes**: `'Song Name'` not `"Song Name"`
2. **Add Commas**: Every song except the last needs a comma `,`
3. **Keep the Format**: `{'name': ..., 'artist': ..., 'genre': ...}`
4. **Test After**: Restart the app to see changes

---

## 🎨 Popular Genre Options

Choose from these or use your own:
- Pop
- Rock
- Hip-Hop
- EDM
- R&B
- Country
- Jazz
- Classical
- Bollywood
- K-Pop
- Indie
- Alternative
- Metal
- Folk
- Electronic
- Reggae

---

## 💡 Pro Tips

1. **Mix Genres**: Add variety within each emotion
2. **Personal Favorites**: Add songs you actually like!
3. **Language Variety**: Add songs in any language
4. **Keep Backups**: Save the original file before editing
5. **Test Often**: Add a few songs, test, then add more

---

## 🔄 After Adding Songs

### To See Your Changes:
1. **Save the file** (Ctrl + S)
2. **Restart the server**:
   - Press Ctrl+C in terminal
   - Run: `.\venv\Scripts\python.exe app.py`
3. **Refresh browser** (F5)
4. **Test your new songs!**

---

## ❓ Quick Examples

### Just tell me what you want and I'll add it!

**Example Request:**
> "Add these songs to Happy:
> - Senorita by Shawn Mendes
> - Shape of You by Ed Sheeran
> - Cheap Thrills by Sia"

**I'll respond with the code and update the file!**

---

## 🎵 Ready to Add Your Music?

**Tell me:**
1. Which emotion? (Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral)
2. What songs? (Title - Artist)
3. Replace all or add to existing?

**Example:**
```
Add to Happy:
- Senorita - Shawn Mendes
- Beautiful - Bazzi
- Good Time - Owl City

Add to Sad:
- Perfect - Ed Sheeran
- Say Something - A Great Big World
```

---

**I'll update the file for you immediately!** 🚀

Just tell me your songs and I'll add them!
