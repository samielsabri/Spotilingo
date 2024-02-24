import requests
import os

import backend.utilities.lyrics_processing as lyrp

class MusixmatchService:
    """Service to interact with the Musixmatch API."""
    BASE_URL = 'https://api.musixmatch.com/ws/1.1/'

    def __init__(self):
        self.api_key = os.getenv('MUSIXMATCH_TOKEN')

    def get_lyrics(self, song, timeout=10):
        """Performs an alternative search for lyrics using the Musixmatch API."""
        params = {
            'q_track': song.processed_title,
            'q_artist': song.processed_artist,
            'apikey': self.api_key
        }
        response = requests.get(f"{self.BASE_URL}matcher.lyrics.get", params=params, timeout=timeout)

        if response.status_code == 200:
            data = response.json()
            if "lyrics" in data["message"]["body"]:
                lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
                return lyrp.process_alternative_lyrics(lyrics.strip())
            print("No lyrics found for the given track and artist.")
            return None
        
        print("Error occurred during API request.")
        return None
        