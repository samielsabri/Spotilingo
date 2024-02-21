import langdetect as ld
from .language_detector import ILanguageDetector

class LdDetectionError(Exception):
    """Custom exception for LangDetect detection errors."""
    def __init__(self, message, text=None):
        super().__init__(message)
        self.message = message
        self.text = text

    def __str__(self):
        """
        String representation of the error, including the text if available.
        """
        if self.text:
            return f"LdDetectionError: {self.message} | Text: {self.text}"
        return f"LdDetectionError: {self.message}"

class LdDetector(ILanguageDetector):
    """Language detector using langdetect library."""
    def __init__(self):
        """Initializes the LdLanguageDetector."""
        ld.DetectorFactory.seed = 0

    def detect_languages(self, line):
        """Detects the language of the given text using langdetect."""
        try:
            possible_languages = ld.detect_langs(line)
            most_probable_language = possible_languages[0]
            language = most_probable_language.lang
            confidence = most_probable_language.prob
            return language, confidence
        except Exception as e:
            raise LdDetectionError("Language detection failed", text=line) from e