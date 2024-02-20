# frameworks_and_drivers/web_app/app.py
import sys
import os

from interface_adapters.gateways.spotify_service import SpotifyService

from flask import Flask, request, jsonify, redirect, session, url_for, render_template
from dotenv import load_dotenv



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

# genius_service = GeniusService()

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
    if 'token_info' not in session:
        return redirect('/login')
    return render_template('main.html')  # Create a main.html template with buttons

@app.route('/get-liked-songs', methods=['POST'])
def get_liked_songs():
    """Fetch the last 10 liked songs for the logged-in user."""
    try:
        if 'token_info' not in session:
            # User not logged in, start the OAuth flow
            return redirect(url_for('login'))
        
        liked_songs = spotify_service.get_liked_songs(session)
        
        songs_data = [{
            'spotify_id': song.id,
            'title': song.title,
            'processed_title': song.processed_title,
            'artist': song.primary_artist,
            'processed_artist': song.processed_artist,
            'secondary_artist': song.secondary_artist,
            'other_artists': song.other_artists,
            'popularity': song.popularity
        } for song in liked_songs]
        
        return jsonify(songs_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)

