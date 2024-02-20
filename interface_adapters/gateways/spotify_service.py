import spotipy
from spotipy.oauth2 import SpotifyOAuth
import utilities.string_processing as string_processing
from domain.entities.song import Song


class SpotifyService:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.oauth_manager = SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope="user-library-read")
        self.sp = None
        
    def get_spotify_client(self, session):
        if 'token_info' not in session:
            raise Exception("User not logged in")
        # Check if the session token has expired
        if self.oauth_manager.is_token_expired(session['token_info']):
            session['token_info'] = self.oauth_manager.refresh_access_token(session['token_info']['refresh_token'])
        self.sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        return self.sp
    


    def get_liked_songs(self, session):
        spotify_client = self.get_spotify_client(session)
        results = spotify_client.current_user_saved_tracks(limit=10)
        songs = []
        for item in results['items']:
            track = item['track']
            artists = track['artists']
            if len(artists) > 1:
                secondary_artist = artists[1]['name']
                other_artists = [artist['name'] for artist in artists[2:]]
            else:
                secondary_artist = ""
                other_artists = []

            processed_name, processed_artist = string_processing.process_input(track['name'], track['artists'][0]['name'])
            
            song = Song(track['id'], 
                        track['name'], 
                        processed_name,
                        track['artists'][0]['name'],
                        processed_artist,
                        secondary_artist,
                        other_artists,
                        track['popularity'],
                        )
            songs.append(song)
        return songs
