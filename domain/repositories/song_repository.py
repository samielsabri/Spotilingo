"""Song Repository Interface"""
from domain.entities.song import Song

class ISongRepository:
    """Interface for the song repository."""
    def add_song(self, song: Song):
        """Add a song to the repository."""
        raise NotImplementedError

    def get_song_by_id(self, spotify_id: str) -> Song:
        """Get a song by its Spotify ID."""
        raise NotImplementedError