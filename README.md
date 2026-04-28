#  Mood Playlist Generator

By Housni Saouid  
CS 1051 — Intro to Python | Final Project | 2026

#  Overview

Mood Playlist Generator is a terminal-based Python program that asks you how you're feeling and instantly generates real song playlists that match your mood powered by the Spotify API.

Tell it you're happy, sad, hype, chill, angry, romantic, anxious, or motivated, or just type any mood you want and it will return multiple curated playlists you can browse and save.

---

# Demo Video

> **[INSERT YOUR VIDEO URL HERE]**

---

# Features

-  8 built-in moods (Happy, Sad, Hype, Chill, Angry, Romantic, Anxious, Motivated)
-  Free-text mood input — type any mood you feel
-  Genre filter, narrow results by genre (hip-hop, lo-fi, pop, metal, etc.)
-  3 playlist options per search so you can pick your favorite
-  Save to file l exports your chosen playlist as a `.txt` file with song titles, artists, albums, and Spotify links
-  Colorful terminal UI,  energy bars, mood indicators, and styled output

---

## How to Run

# 1. Clone the repo
```bash
git clone https://github.com/Housni-S-S/MoodPlaylistGenerator
cd mood-playlist-generator
```

# 2. Install dependencies
```bash
pip install -r requirements.txt
```

# 3. Run the program
```bash
python mood_playlist.py
```





#  Requirements
 Python 3.8+
spotipy` library (`pip install spotipy`)
 A Spotify Developer account (credentials are already configured in the script)



# Project Structure


mood-playlist-generator/
 mood_playlist.py     # Main program
 requirements.txt     # Python dependencies
 README.md            # This file




#  How It Works

1. You type a mood
2. Optionally filter by genre
3. The program searches Spotify using mood-matched keywords and audio-feature targeting (energy, valence, tempo)
4. Three playlist options are displayed in the terminal
5. You choose one to save as a `.txt` file



# What I Learned

- How to authenticate with and use the Spotify Web API via the `spotipy` Python library
- How Spotify's audio features (energy, valence, tempo) map to emotional qualities in music
- How to structure a multi-step CLI program with clean user prompts
- How to handle API errors gracefully and deduplicate search results
- How to format terminal output with ANSI color codes



# Challenges I Faced

- Spotify's audio feature endpoint  requires OAuth user authentication, which was beyond the scope of a terminal app. I worked around this by targeting mood through keyword searches and query tuning rather than direct audio-feature filtering.
- Getting consistent, mood-accurate results took several rounds of keyword refinement per mood.
- Making the terminal output look clean and readable without a GUI required learning ANSI escape codes.



# Outcome Achieved

BEST outcome — All three tiers completed:
- Working mood input → Spotify song recommendations
- Save playlist to `.txt` file
- Polished terminal UI with color and formatting
- Genre filter
- 3 playlist options to choose from


