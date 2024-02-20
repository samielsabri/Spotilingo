class FetchLikedSongs:
    def __init__(self, spotify_service):
        self.spotify_service = spotify_service

    def execute(self, user_token):
        return self.spotify_service.get_liked_songs(user_token)