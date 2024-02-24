"""Module for the AnalyzeSongLanguages use case."""
MIN_LINE_LENGTH = 10
CONFIDENCE_THRESHOLD = 0.85
INCLUDE_LANGUAGE_THRESHOLD = 0.10
INCLUDE_LANGUAGE_THRESHOLD_SMALL_SAMPLE = 0.25


class AnalyzeSongLanguages:
    """Use case to analyze the languages of a song's lyrics."""
    def __init__(self, primary_detector, fallback_detector, fallback_fallback_detector):
        self.primary_detector = primary_detector
        self.fallback_detector = fallback_detector
        self.fallback_fallback_detector = fallback_fallback_detector
        self.confidence_threshold = CONFIDENCE_THRESHOLD
        self.include_language_threshold = INCLUDE_LANGUAGE_THRESHOLD
        self.include_language_threshold_small_sample = INCLUDE_LANGUAGE_THRESHOLD_SMALL_SAMPLE


    def execute(self, song):
        """Executes the use case."""
        languages = []

        for line in song.lyrics:
            language, confidence = self.primary_detector.detect_languages(line)
            if confidence < self.confidence_threshold:
                language, confidence = self.fallback_detector.detect_languages(line)
                if confidence < self.confidence_threshold:
                    language, confidence = self.fallback_fallback_detector.detect_languages(line)
                    if confidence < self.confidence_threshold:
                        continue
            languages.append(language)

        language_prop = create_language_prop(languages)


        final_languages = []

        for language, prop in language_prop.items():
            if len(languages) < 15:
                if prop >= INCLUDE_LANGUAGE_THRESHOLD_SMALL_SAMPLE:
                    final_languages.append(language)
            else:
                if prop >= INCLUDE_LANGUAGE_THRESHOLD:
                    final_languages.append(language)

        song.languages = final_languages
    
def create_language_prop(languages):
    """Creates a dictionary with the proportion of each language in the list."""
    language_count = {}
    total_count = len(languages)


    for language in languages:
        if language not in language_count:
            language_count[language] = 1
        else:
            language_count[language] += 1


    language_prop = {lang: count / total_count for lang, count in language_count.items()}


    return language_prop