class ILanguageDetector:
    """Interface for language detection service."""
    def detect_languages(self, line):
        """Detects the language of the given text."""
        raise NotImplementedError