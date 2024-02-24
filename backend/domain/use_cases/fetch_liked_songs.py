"""Module for the FetchLikedSongs use case."""
class FetchLikedSongs:
    """Use case to fetch the last n liked songs for the logged-in user."""
    def __init__(self, spotify_service):
        """Initializes a new instance of the FetchLikedSongs class."""
        self.spotify_service = spotify_service

    def execute(self, user_token):
        """Fetch the last n liked songs for the logged-in user."""
        return self.spotify_service.get_liked_songs(user_token)