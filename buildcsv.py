import csv
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# 1. Load Spotify Credentials
load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)

# 2. Pick genres to collect
GENRES = [
    "pop", "rock", "hip hop", "lofi", "dance", "r&b",
    "classical", "edm", "jazz", "sad", "chill", "study"
]

# 3. Search Spotify & collect songs
def get_songs_by_genre(genre, limit=100):
    print(f"Collecting songs for genre: {genre}")

    results = sp.search(q=f"genre:{genre}", type="track", limit=50)
    tracks = results["tracks"]["items"]

    songs = []
    for t in tracks:
        songs.append({
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "genre": genre
        })

    return songs

# 4. Save everything to a CSV file
csv_file = "music_data.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "artist", "genre"])
    writer.writeheader()

    for g in GENRES:
        rows = get_songs_by_genre(g)
        writer.writerows(rows)

print(f"\nDONE! CSV saved as {csv_file}")
