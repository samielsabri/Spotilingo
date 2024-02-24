"""This module contains the Song class, which represents a song entity."""
class Song:
    """Represents a song entity."""
    def __init__(self, spotify_id, title, processed_title, primary_artist, processed_artist, secondary_artist, other_artists, popularity, lyrics = None, languages = None):
        """Initializes a new instance of the Song class.

        :param spotify_id: The unique Spotify identifier of the track.
        :param title: The title of the track.
        :param processed_title: The processed title of the track.
        :param primary_artist: The primary artist of the track.
        :param processed_artist: The primary artist of the track, but after string processing.
        :param secondary_artist: The secondary artist of the track.
        :param other_artists: The other artists of the track.
        :param popularity: The popularity of the track.
        :param lyrics: The lyrics of the track.
        :param languages: The languages of the track.
        """
        self.spotify_id = spotify_id
        self.title = title
        self.processed_title = processed_title
        self.primary_artist = primary_artist
        self.processed_artist = processed_artist
        self.secondary_artist = secondary_artist
        self.other_artists = other_artists
        self.popularity = popularity

        self.lyrics = lyrics if lyrics is not None else "No lyrics found"
        self.languages = languages if languages is not None else []

    def __repr__(self):
        """
        Returns a string representation of the song, including its title, primary artist, and language(s).
        """
        return f"'{self.title}' by {self.primary_artist} ({self.languages}) with lyrics '{self.lyrics}'."