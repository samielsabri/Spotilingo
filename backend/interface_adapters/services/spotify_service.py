"""This module is responsible for interacting with the Spotify API."""
import spotipy
import datetime
import time
from spotipy.oauth2 import SpotifyOAuth
import backend.utilities.string_processing as string_processing
from backend.domain.entities.song import Song

LIMIT_LIKED_SONGS = 50
LIMIT_LISTENING_HISTORY = 50
LIMIT_TOP_SONGS = 50

class SpotifyService:
    """This class is responsible for interacting with the Spotify API."""
    def __init__(self, client_id, client_secret, redirect_uri):
        self.oauth_manager = SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope="user-library-read, user-read-recently-played, playlist-read-private, user-top-read")
        self.sp = None
        
    def get_spotify_client(self, session):
        """Get the Spotify client using the session token."""
        if 'token_info' not in session:
            raise Exception("User not logged in")
        
        token_info = session['token_info']
        
        if self.oauth_manager.is_token_expired(token_info):
            token_info = self.oauth_manager.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
            
        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        return self.sp
    
    def get_liked_songs(self, session):
        """Fetch the liked songs for the logged-in user."""
        spotify_client = self.get_spotify_client(session)
        total_songs = []
        iter = 0
        start_time = time.time()
        
        while True:
            if iter > 0 and iter % 10 == 0:  # Check token expiration every 10 iterations
                spotify_client = self.get_spotify_client(session)  # Refresh client if token expired
            
            if time.time() - start_time >= 3540:  # Check if 59 minutes have passed (3540 seconds)
                # Refresh client if 59 minutes have passed
                spotify_client = self.get_spotify_client(session)
                start_time = time.time()  # Reset start time

            offset = iter * 50
            iter += 1
            cur_group = spotify_client.current_user_saved_tracks(limit=50, offset=offset)['items']
            print(f"Current group: {len(cur_group)}")

            if not cur_group:
                break
            
            songs = self.process_results(cur_group)
            total_songs.extend(songs)


            if (len(cur_group) < 50):
                break
            
        return total_songs
    
    def get_listening_history(self, session):
        """Fetch the listening history of the logged-in user."""
        spotify_client = self.get_spotify_client(session)
        total_songs = []
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(days=30)
        after = int(start_time.timestamp()) * 1000
        
       
        results = spotify_client.current_user_recently_played(limit=LIMIT_LISTENING_HISTORY, after=after)['items']
        
        songs = self.process_results(results)
        total_songs.extend(songs)
            
        
        return total_songs
    

    def get_top_songs(self, session, time_range):
        """Fetch the top songs of the logged-in user."""
        spotify_client = self.get_spotify_client(session)
        total_songs = []
        results = spotify_client.current_user_top_tracks(limit=LIMIT_TOP_SONGS, offset=0, time_range=time_range)['items']
        songs = self.process_results(results, is_top_songs=True)
        total_songs.extend(songs)
        return total_songs
    
    def get_user_playlists(self, session):
        """Fetch the playlists of the logged-in user."""
        spotify_client = self.get_spotify_client(session)
        playlists = []
        results = spotify_client.current_user_playlists()
        playlists.extend(results['items'])
        while results['next']:
            results = spotify_client.next(results)
            playlists.extend(results['items'])
        return playlists
    
    def get_playlist_songs(self, session, playlist_id):
        """Fetch the songs from a specific playlist."""
        spotify_client = self.get_spotify_client(session)
        total_songs = []
        offset = 0
        while True:
            results = spotify_client.playlist_tracks(playlist_id, offset=offset)
            
            if not results['items']:
                break

            songs = self.process_results(results['items'])
            total_songs.extend(songs)

            offset += len(results['items'])
        
        return total_songs



    def process_results(self, results, is_top_songs=False):
        songs = []
        for item in results:
            track = item['track'] if not is_top_songs else item
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





