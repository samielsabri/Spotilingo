import requests
from lyricsgenius import Genius
from dotenv import load_dotenv
import os

load_dotenv()

class GeniusService:
    BASE_URL = "https://api.genius.com"

    def __init__(self):
        self.genius = os.getenv('GENIUS_TOKEN')
    
    # def _get(self, path, params=None):
    #     """Private method to make a GET request to the Genius API."""
    #     headers = {"Authorization": f"Bearer {self.genius_token}"}
    #     response = requests.get(f"{self.BASE_URL}/{path}", params=params, headers=headers)
    #     response.raise_for_status()
    #     return response.json()
    
    def get_lyrics(self, song):
        song = self.genius.search_song(song.title, song.artist)
        return song.lyrics if song else None