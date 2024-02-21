import utilities.string_processing as strp
import utilities.lyrics_processing as lyrp

class FetchLyrics:
    """Use case to fetch the lyrics for a song."""
    def __init__(self, genius_service, musixmatch_service):
        self.genius_service = genius_service
        self.musixmatch_service = musixmatch_service

    def execute(self, song):
        """Fetch the lyrics for a song. If the Genius API fails (in all its approaches), use the Musixmatch API. If both fail, return None."""
        lyrics = self.genius_service.get_lyrics(song)
        if lyrics == "Different approaches needed.":
            lyrics = self.genius_service.try_different_approaches(song)
            if lyrics == "Alternative search needed.":
                lyrics = self.musixmatch_service.get_lyrics(song)
                if lyrics is not None:
                    song.lyrics = lyrics
                    return
                else:
                    song.lyrics = "No lyrics found." # maybe raise an exception here
                    return
            if lyrics is not None:
                song.lyrics = lyrics
                return
            else:
                song.lyrics = "No lyrics found." # maybe raise an exception here
                return
        if lyrics == "Alternative search needed.":
            lyrics = self.musixmatch_service.get_lyrics(song)
            if lyrics is not None:
                song.lyrics = lyrics
                return
            else:
                song.lyrics = "No lyrics found." # maybe raise an exception here
                return
        song.lyrics = lyrics
        return
    
    