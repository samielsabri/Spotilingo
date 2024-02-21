# frameworks_and_drivers/web_app/app.py
import os
import time
from flask import Flask
from flask import request, jsonify, redirect, session, url_for, render_template
from dotenv import load_dotenv

from domain.use_cases.fetch_liked_songs import FetchLikedSongs
from domain.use_cases.fetch_lyrics import FetchLyrics
from interface_adapters.services.spotify_service import SpotifyService
from interface_adapters.services.genius_service import GeniusService
from interface_adapters.services.musixmatch_service import MusixmatchService




load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://localhost:5000/callback'

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# Configure your SpotifyService with actual credentials
spotify_service = SpotifyService(client_id=CLIENT_ID,
                                 client_secret=CLIENT_SECRET,
                                 redirect_uri=REDIRECT_URI)

genius_service = GeniusService()
musixmatch_service = MusixmatchService()

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
        
        start_time = time.time()
        fetch_liked_songs_use_case = FetchLikedSongs(spotify_service)
        fetch_lyrics_use_case = FetchLyrics(genius_service, musixmatch_service)



        liked_songs = fetch_liked_songs_use_case.execute(session)

        for song in liked_songs:
            song_start_time = time.time()
            fetch_lyrics_use_case.execute(song)
            if song.lyrics != "No lyrics found":
                song.languages = language_detector.detect_languages(lyrics)
            song_end_time = time.time()
            print(f"Time to fetch lyrics and languages for {song.title}: {song_end_time - song_start_time} seconds")
        
        songs_data = [{
            'spotify_id': song.id,
            'title': song.title,
            'processed_title': song.processed_title,
            'artist': song.primary_artist,
            'processed_artist': song.processed_artist,
            'secondary_artist': song.secondary_artist,
            'other_artists': song.other_artists,
            'popularity': song.popularity,
            'lyrics': song.lyrics
        } for song in liked_songs]

        end_time = time.time()
        songs_data_length = len(songs_data)
        print(f"Total time to fetch all liked {songs_data_length} songs and lyrics: {end_time - start_time} seconds.")
        
        return jsonify(songs_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)

