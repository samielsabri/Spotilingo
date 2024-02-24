import os
from dotenv import load_dotenv

from backend.domain.entities.song import Song
from backend.interface_adapters.services.genius_service import GeniusService
from backend.interface_adapters.services.musixmatch_service import MusixmatchService
from backend.domain.use_cases.fetch_lyrics import FetchLyrics
from backend.domain.use_cases.analyze_song_languages import AnalyzeSongLanguages
from backend.domain.use_cases.analyze_songs import AnalyzeSongs
from backend.frameworks_and_drivers.repository.sqlite_song_repository import SQLiteSongRepository
from backend.frameworks_and_drivers.config import FASTTEXT_MODEL_PATH

from backend.interface_adapters.services.fasttext_language_detector import FastTextDetector
from backend.interface_adapters.services.langid_language_detector import LangIDDetector
from backend.interface_adapters.services.ld_language_detector import LdDetector



if __name__ == '__main__':

    load_dotenv()
    db_path = os.getenv('DB_PATH')
    genius_service = GeniusService()
    musixmatch_service = MusixmatchService()
    fasttext_detector = FastTextDetector(FASTTEXT_MODEL_PATH)
    langid_detector = LangIDDetector()
    ld_detector = LdDetector()
    fetch_lyrics_use_case = FetchLyrics(genius_service, musixmatch_service)
    analyze_song_languages_use_case = AnalyzeSongLanguages(fasttext_detector, langid_detector, ld_detector)
    
    songs = [Song("202930102", "Afeto (Ankhoi Remix)", "afeto---ankhoi-remix", 
                "Mayra Andrade", "mayra-andrade", "Ankhoi", [], 100), 
                Song("456", "CONTIGO (with Tiesto)", "contigo-(with-tiesto)", "KAROL G", "karol-g",
                     "Tiesto", [], 100)]
    
    song_repository = SQLiteSongRepository(db_path)


    # analyze_songs_use_case = AnalyzeSongs(songs, fetch_lyrics_use_case, analyze_song_languages_use_case, song_repository)
    # analyze_songs_use_case.execute()