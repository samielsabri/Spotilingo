class FetchPlaylistsUseCase:
    def __init__(self, spotify_service):
        """Initializes a new instance of the FetchPlaylistSongsUseCase class."""
        self.spotify_service = spotify_service

    def execute(self, user_token):
        """Fetch songs from the specified playlist."""
        return self.spotify_service.get_user_playlists(user_token)