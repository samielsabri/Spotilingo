"""This module contains the SQLiteSongRepository class."""
import sqlite3
from domain.entities.song import Song
from domain.repositories.song_repository import ISongRepository

class SQLiteSongRepository(ISongRepository):
    """A SQLite implementation of the song repository."""
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_db()

    def initialize_db(self):
        """Initializes the database with the songs table if it does not exist."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS songs (
                        spotify_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        processed_title TEXT NOT NULL,
                        primary_artist TEXT NOT NULL,
                        processed_artist TEXT NOT NULL,
                        secondary_artist TEXT,
                        other_artists TEXT,
                        popularity INTEGER,
                        lyrics TEXT,
                        languages TEXT
                        );''')
        connection.commit()
        connection.close()

    def add_song(self, song: Song):
        """Adds a song to the repository."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            lyrics_str = '\n'.join(song.lyrics) if song.lyrics else None
            languages_str = ','.join(song.languages) if song.languages else None
            cursor.execute('''INSERT INTO songs (spotify_id, title, processed_title, primary_artist, processed_artist, secondary_artist, other_artists, popularity, lyrics, languages) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', 
                           (song.spotify_id, song.title, song.processed_title, song.primary_artist, song.processed_artist,
                            song.secondary_artist, ','.join(song.other_artists), song.popularity, lyrics_str, languages_str))
            conn.commit()

    def get_song_by_id(self, spotify_id: str) -> Song:
        """Retrieves a song from the repository by its Spotify ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM songs WHERE spotify_id = ?', (spotify_id,))
            row = cursor.fetchone()
            if row:
                lyrics_list = row[8].split('\n') if row[8] else None
                languages_list = row[9].split(',') if row[9] else None
                return Song(spotify_id=row[0], title=row[1], processed_title=row[2], primary_artist=row[3], 
                            processed_artist=row[4], secondary_artist=row[5], other_artists=row[6], popularity=row[7],
                              lyrics=lyrics_list, languages=languages_list)
            return None