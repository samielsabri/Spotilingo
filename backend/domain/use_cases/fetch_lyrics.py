"""Use case to fetch the lyrics for a song."""
class FetchLyrics:
    """Use case to fetch the lyrics for a song."""
    def __init__(self, genius_service, musixmatch_service, timeout=10):
        """Initializes a new instance of the FetchLyrics class."""
        self.genius_service = genius_service
        self.musixmatch_service = musixmatch_service
        self.timeout = timeout

    def execute(self, song):
        """Fetch the lyrics for a song."""
        try:
            lyrics = self.genius_service.get_lyrics(song)
            if not lyrics or lyrics == "Different approaches needed.":
                lyrics = self.genius_service.try_different_approaches(song)
                
            if not lyrics or lyrics == "Alternative search needed.":
                lyrics = self.musixmatch_service.get_lyrics(song)
            
            song.lyrics = lyrics if lyrics else None
        
        except Exception as e:  # Consider catching more specific exceptions
            print(f"An error occurred while fetching lyrics: {e}")
            song.lyrics = None
    
    