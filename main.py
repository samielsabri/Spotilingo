from domain.entities.song import Song
from interface_adapters.gateways.genius_service import GeniusService
from interface_adapters.gateways.musixmatch_service import MusixmatchService
from domain.use_cases.fetch_lyrics import FetchLyrics

if __name__ == '__main__':
    
    genius_service = GeniusService()
    musixmatch_service = MusixmatchService()
    fetch_lyrics_use_case = FetchLyrics(genius_service, musixmatch_service)
    song = Song("123", "Outété", "outete", "Keen' V", "keen-v", "", [], 100)
    fetch_lyrics_use_case.execute(song)
    print(song)