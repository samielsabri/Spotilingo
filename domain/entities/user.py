class User:
     def __init__(self, spotify_user_id, access_token=None, refresh_token=None):
        """
        Initializes a new User instance.

        :param spotify_user_id: A unique identifier for the user.
        :param access_token: Token for accessing Spotify's Web API on behalf of the user.
        :param refresh_token: Token for refreshing the access token.
        """
        self.spotify_user_id = spotify_user_id
        self.access_token = access_token
        self.refresh_token = refresh_token