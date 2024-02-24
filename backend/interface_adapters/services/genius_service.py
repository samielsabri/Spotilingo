"""This module contains the GeniusService class, which is a service to interact with the Genius API."""
import os
import time
import requests
from lyricsgenius import Genius
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from romkan import to_hiragana

import backend.utilities.string_processing as strp
import backend.utilities.lyrics_processing as lyrp

BASE_URL = "https://api.genius.com"
FUZZY_THRESHOLD = 85
MAX_RETRIES = 3

class GeniusService:
    """Service to interact with the Genius API."""
    def __init__(self):
        load_dotenv()
        self.base_url = BASE_URL 
        self.genius_token = os.getenv('GENIUS_TOKEN')
        self.genius = Genius(self.genius_token, timeout=10)
        self.genius.verbose = True
    
    def _get(self, path, params=None, headers=None, timeout=10):
        """Private method to make a GET request to the Genius API."""
        requrl = '/'.join([self.base_url, path])
        token = "Bearer {}".format(self.genius_token)
        if headers:
            headers['Authorization'] = token
        else:
            headers = {"Authorization": token}

        response = requests.get(url=requrl, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()

        return response.json()
    
    def get_lyrics(self, song):
        """Get the lyrics for a song from the Genius API."""
        self.genius.skip_non_songs = True
        self.genius.replace_default_terms = ['track\\s?list', 'album art(work)?', 'liner notes',
                                    'booklet', 'credits', 'interview', 'skit',
                                    'instrumental', 'setlist', 'New Music?']
        
        retries = 0
        while retries < MAX_RETRIES:
            try:
                # First, try searching with the provided artist_name and track_name
                genius_track = self.genius.search_song(song.processed_title, song.processed_artist)

                if genius_track is not None:
                    # Check if the result matches the artist_name and track_name
                    if self.is_result_valid(song, genius_track):
                        # perfect match
                        processed_lyrics = lyrp.process_lyrics(genius_track.lyrics)
                        if lyrp.is_potential_arabizi(processed_lyrics):
                            # other lyrics platform has better Arabic lyrics
                            return "Alternative search needed."
                        return processed_lyrics
                    else:
                        # found something but it is not the requested song
                        processed_lyrics = lyrp.process_lyrics(self.wrong_result_alternative_search(song))
                        if processed_lyrics is None:
                            return "Different approaches needed."
                        if lyrp.is_potential_arabizi(processed_lyrics):
                            # other lyrics platform has better Arabic lyrics
                            return "Alternative search needed."
                        return processed_lyrics
                else:
                    return "Different approaches needed."

            except requests.exceptions.Timeout:
                # Retry on timeout
                retries += 1
                time.sleep(5)  # Wait for 5 seconds before retrying

        print('Exceeded maximum number of retries. No lyrics found for the given track and artist')
        return None
    
    def is_result_valid(self, spotify_track, genius_track):
        """Check if the result from the Genius API matches the requested Spotify song."""
        genius_track_processed_title, genius_track_processed_artist = strp.process_input(genius_track.title, genius_track.primary_artist.name)
        fuzzy_track = fuzz.partial_ratio(genius_track_processed_title, spotify_track.processed_title)
        fuzzy_artist = fuzz.partial_ratio(genius_track_processed_artist, spotify_track.processed_artist)
        if fuzzy_track < FUZZY_THRESHOLD or fuzzy_artist < FUZZY_THRESHOLD:
            return False
        return True

    def wrong_result_alternative_search(self, song):
        """Search for the song using the artist's ID and find the best match. This function will only be called if the initial search returned a wrong result."""
        # find artist ID
        find_id = self._get("search", {'q': song.processed_artist})
        artist_id = None
        for hit in find_id["response"]["hits"]:
            if song.processed_artist in strp.normalize_diacritics_and_special_chars(hit["result"]["primary_artist"]["name"]).lower().replace(' ', '-').replace("'", "").replace("’", ""):
                artist_id = hit["result"]["primary_artist"]["id"]
                break
        if artist_id is None:
            return None
        
        artist_songs = self.genius.artist_songs(artist_id, sort='popularity', per_page=50)
        found_track = self.find_track_in_artist_songs(artist_songs, song)

        if found_track is None:
            return None
        found_track_id = found_track['id']
        track_lyrics = self.genius.lyrics(found_track_id)
        return track_lyrics
    
    def find_track_in_artist_songs(self, artist_songs, song):
        """Find the best match for the song in the artist's songs. This function will only be called if the initial search returned a wrong result."""
        best_match = None
        best_match_score = 0


        for artist_song in artist_songs['songs']:
            full_title = artist_song['full_title']
            processed_full_title = strp.preprocess_full_title(full_title)


            similarity_score = fuzz.partial_ratio(processed_full_title, song.processed_title)
            
            # if len(artist_song['featured_artists']) != 0:
                # featured = artist_song['featured_artists'][0]['name'].lower().replace(' ', '-')


            if len(artist_song['featured_artists']) == 0 and song.secondary_artist != "":
                similarity_score -= 20


            if len(artist_song['featured_artists']) != 0:
                for artist in artist_song['featured_artists']:
                    artist = artist['name'].lower().replace(' ', '-')
                    if artist in song.processed_title or artist in song.secondary_artist or \
                        any(artist in other_artist for other_artist in song.other_artists):
                        similarity_score += 20
            
            if similarity_score > best_match_score:
                best_match_score = similarity_score
                best_match = artist_song
        
        if best_match_score < FUZZY_THRESHOLD:
            return None
        
        return best_match
    

    def try_different_approaches(self, song, attempt=0):
        """Try different approaches to find the lyrics for a song. The approaches are:
        - Attempt 0: Try searching through artist's songs
        - Attempt 1: Deal with features
        - Attempt 2: Convert to hiragana
        - Attempt 3: Alternative search on a different platform"""


        if attempt == 0:
            processed_lyrics = lyrp.process_lyrics(self.wrong_result_alternative_search(song))
            if processed_lyrics is not None:
                if lyrp.is_potential_arabizi(processed_lyrics): 
                    # other lyrics platform has better arabic lyrics
                    return "Alternative search needed."
                return processed_lyrics
            processed_track_name = song.processed_title
        elif attempt == 1:
            processed_track_name = strp.process_track_name_features(song.processed_title)
        elif attempt == 2:
            processed_track_name = to_hiragana(song.title.lower())
        elif attempt == 3:
            return "Alternative search needed."

        # Attempt to search with the processed track name
        genius_track = self.genius.search_song(processed_track_name, song.processed_artist)


        if genius_track is not None and self.is_result_valid(song, genius_track):
            processed_lyrics = lyrp.process_lyrics(genius_track.lyrics)
            if lyrp.is_potential_arabizi(processed_lyrics): # other lyrics platform has better arabic lyrics
                return "Alternative search needed."
            return processed_lyrics
        elif attempt < 3:
            return self.try_different_approaches(song, attempt + 1)
        else:
            print('No lyrics found for the given track and artist')
            return None


