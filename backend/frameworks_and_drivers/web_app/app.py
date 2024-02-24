# frameworks_and_drivers/web_app/app.py
import os
import time
from flask import Flask
from flask import request, jsonify, redirect, session, url_for, render_template
from dotenv import load_dotenv

from backend.domain.use_cases.fetch_liked_songs import FetchLikedSongs
from backend.domain.use_cases.fetch_lyrics import FetchLyrics
from backend.domain.use_cases.analyze_song_languages import AnalyzeSongLanguages
from backend.domain.use_cases.count_languages import CountLanguages
from backend.domain.use_cases.analyze_songs import AnalyzeSongs
from backend.interface_adapters.services.spotify_service import SpotifyService
from backend.interface_adapters.services.genius_service import GeniusService
from backend.interface_adapters.services.musixmatch_service import MusixmatchService
from backend.interface_adapters.services.fasttext_language_detector import FastTextDetector
from backend.interface_adapters.services.langid_language_detector import LangIDDetector
from backend.interface_adapters.services.ld_language_detector import LdDetector
from backend.interface_adapters.controllers.language_count_controller import LanguageCountController
from backend.interface_adapters.presenters.language_count_presenter import LanguageCountPresenter


from backend.frameworks_and_drivers.config import FASTTEXT_MODEL_PATH
from backend.frameworks_and_drivers.repository.sqlite_song_repository import SQLiteSongRepository





load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://localhost:5000/callback'

# Create a Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Configure your SpotifyService with actual credentials
spotify_service = SpotifyService(client_id=CLIENT_ID,
                                 client_secret=CLIENT_SECRET,
                                 redirect_uri=REDIRECT_URI)

# Configure your lyrics services
genius_service = GeniusService()
musixmatch_service = MusixmatchService()

# Configure your language detectors
fasttext_detector = FastTextDetector(FASTTEXT_MODEL_PATH)
langid_detector = LangIDDetector()
ld_detector = LdDetector()

# Configure your song repository
db_path = os.getenv('DB_PATH')

# Constants
TOP_N = 10


@app.route('/')
def login():
    """Route to start the OAuth flow."""
    print("Generating Spotify auth URL")
    auth_url = spotify_service.oauth_manager.get_authorize_url()
    print(f"Auth URL: {auth_url}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Route for Spotify OAuth callback."""
    print("Received callback from Spotify")
    code = request.args.get('code')
    print(f"Code: {code}")
    token_info = spotify_service.oauth_manager.get_access_token(code)
    print(f"Token info: {token_info}")
    session['token_info'] = token_info  # Save the token info in the session
    return redirect(url_for('main'))

@app.route('/main')
def main():
    """Main route to display the main page."""
    if 'token_info' not in session:
        return redirect('/login')
    return render_template('main.html')  # Create a main.html template with buttons

@app.route('/get-liked-songs', methods=['POST'])
def get_liked_songs():
    """Fetch the last 10 liked songs for the logged-in user."""
    try:
        if 'token_info' not in session:
            # User not logged in, start the OAuth flow
            return redirect(url_for('/login'))
        
        # start_time = time.time()
        fetch_liked_songs_use_case = FetchLikedSongs(spotify_service)
        fetch_lyrics_use_case = FetchLyrics(genius_service, musixmatch_service)
        analyze_song_languages_use_case = AnalyzeSongLanguages(fasttext_detector, langid_detector, ld_detector)
        song_repository = SQLiteSongRepository(db_path)


        analyze_songs_use_case = AnalyzeSongs(session, fetch_liked_songs_use_case, fetch_lyrics_use_case, analyze_song_languages_use_case, song_repository)
        songs = analyze_songs_use_case.execute()

        # for song in liked_songs:
        #     song_start_time = time.time()
        #     song_lyrics_start_time = time.time()
        #     fetch_lyrics_use_case.execute(song)
        #     song_lyrics_end_time = time.time()
        #     if song.lyrics is not None:
        #         song_language_start_time = time.time()
        #         analyze_song_languages_use_case.execute(song)
        #         song_language_end_time = time.time()
        #     else:
        #         song_language_start_time = time.time()
        #         song_language_end_time = time.time()
        #     song_end_time = time.time()
        #     print(f"Time to fetch data for {song.title}: {song_end_time - song_start_time} seconds, lyrics: {song_lyrics_end_time - song_lyrics_start_time} seconds, language: {song_language_end_time - song_language_start_time} seconds.")
        
        # songs_data = [{
        #     'spotify_id': song.spotify_id,
        #     'title': song.title,
        #     'processed_title': song.processed_title,
        #     'artist': song.primary_artist,
        #     'processed_artist': song.processed_artist,
        #     'secondary_artist': song.secondary_artist,
        #     'other_artists': song.other_artists,
        #     'popularity': song.popularity,
        #     'lyrics': song.lyrics,
        #     'languages': song.languages
        # } for song in liked_songs]

        # end_time = time.time()
        # songs_data_length = len(songs_data)
        # print(f"Total time to fetch all liked {songs_data_length} songs and lyrics: {end_time - start_time} seconds.")
        
        count_languages_use_case = CountLanguages()
        language_count_presenter = LanguageCountPresenter()
        language_count_controller = LanguageCountController(count_languages_use_case, language_count_presenter)
        language_counts = language_count_controller.get_language_counts(songs, top_n=TOP_N)

        return jsonify(language_counts)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)

