"""Use case to analyze songs by fetching lyrics and analyzing languages."""

class AnalyzeSongs:
    """Higher-level Use case to analyze songs by fetching lyrics and analyzing languages."""
    def __init__(self, session, fetch_liked_songs_use_case, fetch_lyrics_use_case, analyze_languages_use_case, song_repository):
        """Initializes a new instance of the AnalyzeSongs class."""
        self.session = session
        self.fetch_liked_songs_use_case = fetch_liked_songs_use_case
        self.fetch_lyrics_use_case = fetch_lyrics_use_case
        self.analyze_languages_use_case = analyze_languages_use_case
        self.song_repository = song_repository

    def execute(self):
        """Fetch the liked songs and analyze them by enriching the song object with lyrics and languages"""
        songs = self.fetch_liked_songs_use_case.execute(self.session)

        for song in songs:
            # Check if the song already exists in the repository with lyrics and languages
            existing_song = self.song_repository.get_song_by_id(song.spotify_id)
            if existing_song:
                song.lyrics = existing_song.lyrics
                song.languages = existing_song.languages
            else:
                # Fetch lyrics and analyze languages if the song is not in the repository
                self.fetch_lyrics_use_case.execute(song)
                if song.lyrics is not None:
                    self.analyze_languages_use_case.execute(song)
                self.song_repository.add_song(song)

        return songs