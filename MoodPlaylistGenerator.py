import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import datetime
from dotenv import load_dotenv


#  Spotify Credentials  (loaded from .env file)

load_dotenv()
CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


#  Mood Configuration
#  Each mood maps to:
#    keywords  – search terms sent to Spotify
#    energy    – target audio energy  (0.0–1.0)
#    valence   – target positivity    (0.0–1.0)
#    tempo     – rough BPM hint (used in display only)

MOODS = {
    "1": {
        "label": "😊 Happy",
        "name": "happy",
        "keywords": ["happy upbeat feel good", "good vibes pop", "joyful summer hits"],
        "energy": 0.8,
        "valence": 0.9,
        "tempo": "Fast",
        "genres": ["pop", "dance", "funk"],
        "color": "\033[93m",          
    },
    "2": {
        "label": "😢 Sad",
        "name": "sad",
        "keywords": ["sad emotional songs", "heartbreak ballad", "melancholy indie"],
        "energy": 0.3,
        "valence": 0.2,
        "tempo": "Slow",
        "genres": ["indie", "acoustic", "soul"],
        "color": "\033[94m",          
    },
    "3": {
        "label": "🔥 Hype",
        "name": "hype",
        "keywords": ["hype workout pump up", "high energy rap", "hard hitting bangers"],
        "energy": 0.95,
        "valence": 0.7,
        "tempo": "Very Fast",
        "genres": ["hip-hop", "trap", "edm"],
        "color": "\033[91m",          
    },
    "4": {
        "label": "😌 Chill",
        "name": "chill",
        "keywords": ["chill lo-fi relax", "laid back vibes", "mellow evening"],
        "energy": 0.35,
        "valence": 0.55,
        "tempo": "Slow",
        "genres": ["lo-fi", "chillhop", "ambient"],
        "color": "\033[96m",          
    },
    "5": {
        "label": "😤 Angry",
        "name": "angry",
        "keywords": ["aggressive rock metal", "intense rage rap", "angry hard rock"],
        "energy": 0.95,
        "valence": 0.15,
        "tempo": "Fast",
        "genres": ["metal", "rock", "rap"],
        "color": "\033[31m",          
    },
    "6": {
        "label": "🥰 Romantic",
        "name": "romantic",
        "keywords": ["romantic love songs", "sweet r&b", "slow dance love"],
        "energy": 0.45,
        "valence": 0.75,
        "tempo": "Medium",
        "genres": ["r&b", "soul", "pop"],
        "color": "\033[95m",          
    },
    "7": {
        "label": "😰 Anxious",
        "name": "anxious",
        "keywords": ["calming anxiety relief", "soothing instrumental", "peaceful meditation music"],
        "energy": 0.25,
        "valence": 0.45,
        "tempo": "Very Slow",
        "genres": ["ambient", "classical", "new age"],
        "color": "\033[32m",          
    },
    "8": {
        "label": "💪 Motivated",
        "name": "motivated",
        "keywords": ["motivational success rap", "inspiring workout", "grind hustle beats"],
        "energy": 0.85,
        "valence": 0.8,
        "tempo": "Fast",
        "genres": ["hip-hop", "pop", "electronic"],
        "color": "\033[33m",          
    },
}

# ─────────────────────────────────────────────
#  ANSI helpers
# ─────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
MAGENTA = "\033[95m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", width=55, color=CYAN):
    print(f"{color}{char * width}{RESET}")

def banner():
    clear()
    print(f"\n{MAGENTA}{BOLD}")
    print("  ███╗   ███╗ ██████╗  ██████╗ ██████╗ ")
    print("  ████╗ ████║██╔═══██╗██╔═══██╗██╔══██╗")
    print("  ██╔████╔██║██║   ██║██║   ██║██║  ██║")
    print("  ██║╚██╔╝██║██║   ██║██║   ██║██║  ██║")
    print("  ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██████╔╝")
    print("  ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ ")
    print(f"{RESET}")
    print(f"  {BOLD}{WHITE}🎵  Mood Playlist Generator  🎵{RESET}")
    print(f"  {DIM}Powered by Spotify API{RESET}\n")
    divider()


#  Spotify connection

def connect_spotify():
    try:
        auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth)
        sp.search(q="test", limit=5)
        return sp
    except Exception as e:
        print(f"\n{BOLD}\033[91m  ✗ Could not connect to Spotify: {e}{RESET}")
        print(f"  Check your CLIENT_ID and CLIENT_SECRET in the script.\n")
        return None


#  Song search

def search_songs(sp, mood_data, limit=10, genre_filter=None):
    """
    Search Spotify for songs matching the mood.
    Uses multiple keyword queries and deduplicates results.
    Optionally filters by a genre hint in the query.
    """
    seen_ids  = set()
    tracks    = []

    keywords = mood_data["keywords"]
    if genre_filter:
        keywords = [f"{kw} {genre_filter}" for kw in keywords]

    for query in keywords:
        if len(tracks) >= limit:
            break
        try:
            results = sp.search(q=query, type="track", limit=10)
            for item in results["tracks"]["items"]:
                if item["id"] not in seen_ids and len(tracks) < limit:
                    seen_ids.add(item["id"])
                    tracks.append({
                        "title":   item["name"],
                        "artist":  ", ".join(a["name"] for a in item["artists"]),
                        "album":   item["album"]["name"],
                        "url":     item["external_urls"]["spotify"],
                        "popularity": item.get("popularity", 0),
                    })
        except Exception as e:
            print(f"  Search error for query: {e}")
            continue

    # Sort by popularity so the best tracks surface first
    tracks.sort(key=lambda t: t["popularity"], reverse=True)
    return tracks[:limit]


#  Display playlist

def display_playlist(tracks, mood_data, playlist_num=1):
    color = mood_data["color"]
    print(f"\n  {color}{BOLD}Playlist #{playlist_num}  —  {mood_data['label']} vibes{RESET}")
    print(f"  {DIM}Tempo: {mood_data['tempo']}  |  "
          f"Energy: {'█' * round(mood_data['energy']*10)}{'░' * (10-round(mood_data['energy']*10))}  |  "
          f"Mood: {'█' * round(mood_data['valence']*10)}{'░' * (10-round(mood_data['valence']*10))}{RESET}\n")
    divider()
    for i, t in enumerate(tracks, 1):
        num   = f"{BOLD}{color}{i:>2}.{RESET}"
        title = f"{WHITE}{BOLD}{t['title']}{RESET}"
        artist = f"{DIM}by {t['artist']}{RESET}"
        print(f"  {num}  {title}")
        print(f"       {artist}")
    divider()


#  Save to file

def save_playlist(tracks, mood_data, filename=None):
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"playlist_{mood_data['name']}_{timestamp}.txt"

    lines = [
        "=" * 50,
        f"  🎵 Mood Playlist Generator",
        f"  Mood    : {mood_data['label']}",
        f"  Created : {datetime.datetime.now().strftime('%B %d, %Y  %I:%M %p')}",
        "=" * 50,
        "",
    ]
    for i, t in enumerate(tracks, 1):
        lines.append(f"{i:>2}. {t['title']}")
        lines.append(f"     by {t['artist']}")
        lines.append(f"     Album : {t['album']}")
        lines.append(f"     Link  : {t['url']}")
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n  {GREEN}{BOLD}✓ Playlist saved to: {filename}{RESET}")
    return filename


#  Mood menu

def choose_mood():
    print(f"\n  {BOLD}{WHITE}How are you feeling right now?{RESET}\n")
    for key, mood in MOODS.items():
        print(f"  {mood['color']}{BOLD}  {key}.{RESET}  {mood['label']}")
    print(f"\n  {DIM}Or type your mood freely (e.g. 'nostalgic', 'tired'){RESET}")
    divider()

    choice = input(f"\n  {BOLD}→ Your choice: {RESET}").strip()

    if choice in MOODS:
        return MOODS[choice]

    
    custom_name = choice.lower()
    print(f"\n  {CYAN}Looking for '{custom_name}' vibes on Spotify…{RESET}")
    return {
        "label":    f"✨ {choice.capitalize()}",
        "name":     custom_name,
        "keywords": [f"{custom_name} music", f"{custom_name} songs", f"best {custom_name} playlist"],
        "energy":   0.6,
        "valence":  0.6,
        "tempo":    "Medium",
        "genres":   [],
        "color":    CYAN,
    }


#  Genre filter sub-menu

def choose_genre(mood_data):
    genres = mood_data.get("genres", [])
    if not genres:
        return None

    print(f"\n  {BOLD}{WHITE}Filter by genre? (optional){RESET}\n")
    print(f"  {DIM}  0.  No filter (show all){RESET}")
    for i, g in enumerate(genres, 1):
        print(f"  {CYAN}{BOLD}  {i}.{RESET}  {g.title()}")
    divider()

    raw = input(f"\n  {BOLD}→ Genre choice (0 to skip): {RESET}").strip()
    if raw.isdigit():
        idx = int(raw)
        if 1 <= idx <= len(genres):
            return genres[idx - 1]
    return None


#  Main loop

def main():
    banner()

    print(f"  {DIM}Connecting to Spotify…{RESET}")
    sp = connect_spotify()
    if not sp:
        input("\n  Press Enter to exit.")
        return

    print(f"  {GREEN}{BOLD}✓ Connected to Spotify{RESET}")

    while True:
        mood_data = choose_mood()
        genre_filter = choose_genre(mood_data)
        playlists = []
        num_options = 3   

        print(f"\n  {DIM}Generating {num_options} playlist options…{RESET}\n")

        for pnum in range(1, num_options + 1):
            rotated = {**mood_data, "keywords": mood_data["keywords"][pnum-1:] + mood_data["keywords"][:pnum-1]}
            tracks  = search_songs(sp, rotated, limit=10, genre_filter=genre_filter)
            if tracks:
                playlists.append(tracks)
                display_playlist(tracks, mood_data, playlist_num=pnum)

        if not playlists:
            print(f"\n  \033[91m✗ No songs found. Try a different mood.{RESET}")
        else:
            print(f"\n  {BOLD}{WHITE}Which playlist do you want to save?{RESET}")
            print(f"  {DIM}(Enter 1–{len(playlists)}, or 0 to skip saving){RESET}")
            raw = input(f"\n  {BOLD}→ Choice: {RESET}").strip()

            if raw.isdigit() and 1 <= int(raw) <= len(playlists):
                chosen = playlists[int(raw) - 1]
                save_playlist(chosen, mood_data)

        
        print()
        divider()
        again = input(f"\n  {BOLD}Generate another playlist? (y/n): {RESET}").strip().lower()
        if again != "y":
            break
        banner()

    print(f"\n  {MAGENTA}{BOLD}Thanks for using Mood Playlist Generator! 🎵{RESET}")
    print(f"  {DIM}Happy listening.\n{RESET}")


if __name__ == "__main__":
    main()
