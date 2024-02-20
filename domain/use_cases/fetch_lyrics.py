from interface_adapters.gateways.genius_service import GeniusService
from interface_adapters.gateways.musixmatch_service import MusixmatchService

class FetchLyrics:
    def __init__(self):
        self.genius_service = GeniusService()
        self.musixmatch_service = MusixmatchService()

    def execute(self, song):
        lyrics = self.genius_service.get_lyrics(song)
        if not lyrics:
            lyrics = self.musixmatch_service.alternative_search(song)
        return lyrics