class FetchSongsUseCase:
    """Interface for fetching songs."""
    def execute(self, session):
        """Fetch songs."""
        pass

class FetchLikedSongsUseCase(FetchSongsUseCase):
    """Use case to fetch the last n liked songs for the logged-in user."""
    def __init__(self, spotify_service):
        """Initializes a new instance of the FetchLikedSongs class."""
        self.spotify_service = spotify_service

    def execute(self, user_token):
        """Fetch the last n liked songs for the logged-in user."""
        return self.spotify_service.get_liked_songs(user_token)

class FetchListeningHistoryUseCase(FetchSongsUseCase):
    """Use case to fetch the listening history of the logged-in user."""
    def __init__(self, spotify_service):
        """Initializes a new instance of the FetchListeningHistoryUseCase class."""
        self.spotify_service = spotify_service

    def execute(self, user_token):
        """Fetch the listening history of the logged-in user."""
        return self.spotify_service.get_listening_history(user_token)
    
class FetchTopSongsUseCase(FetchSongsUseCase):
    """Use case to fetch the top songs of the logged-in user."""
    def __init__(self, spotify_service, time_range):
        """Initializes a new instance of the FetchTopSongsUseCase class."""
        self.spotify_service = spotify_service
        self.time_range = str(time_range)
        
    def execute(self, user_token):
        """Fetch the top songs of the logged-in user."""
        return self.spotify_service.get_top_songs(user_token, self.time_range)

class FetchPlaylistSongsUseCase(FetchSongsUseCase):
    """Use case to fetch songs from a specific playlist."""
    def __init__(self, spotify_service, playlist_id):
        """Initializes a new instance of the FetchPlaylistSongsUseCase class."""
        self.spotify_service = spotify_service
        self.playlist_id = playlist_id

    def execute(self, user_token):
        """Fetch songs from the specified playlist."""
        return self.spotify_service.get_playlist_songs(user_token, self.playlist_id)
