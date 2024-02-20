import requests
import os

class MusixmatchService:
    BASE_URL = 'https://api.musixmatch.com/ws/1.1/'

    def __init__(self):
        self.api_key = os.getenv('musixmatch_token')

    def alternative_search(self, spotify_track):
        """Performs an alternative search for lyrics using the Musixmatch API."""
        params = {
            'q_track': spotify_track.processed_title,
            'q_artist': spotify_track.processed_artist,
            'apikey': self.api_key
        }
        response = requests.get(f"{self.BASE_URL}matcher.lyrics.get", params=params)
        if response.status_code == 200:
            data = response.json()
            if "lyrics" in data["message"]["body"]:
                lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
                return lyrics.strip()
            else:
                print("No lyrics found for the given track and artist.")
        else:
            print("Error occurred during API request.")
        return None