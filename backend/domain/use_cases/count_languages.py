"""Module for the CountLanguages use case."""
from collections import Counter

class CountLanguages:
    """Use case to count the languages of a list of songs."""
    def execute(self, songs):
        """Executes the use case."""
        all_languages = [lang for song in songs for lang in song.languages]
        language_counts = Counter(all_languages)
        return language_counts