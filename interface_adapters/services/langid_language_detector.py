from fastlangid.langid import LID
from .language_detector import ILanguageDetector

class LangIDDetectionError(Exception):
    """Custom exception for LangID detection errors."""
    def __init__(self, message, text=None):
        super().__init__(message)
        self.message = message
        self.text = text

    def __str__(self):
        """
        String representation of the error, including the text if available.
        """
        if self.text:
            return f"LangIDDetectionError: {self.message} | Text: {self.text}"
        return f"LangIDDetectionError: {self.message}"

class LangIDDetector(ILanguageDetector):
    """Language detector using langiddetect library."""
    def __init__(self):
        """Initializes the lidLanguageDetector."""
        self.langid = LID()

    def detect_languages(self, line):
        """Detects the language of the given text using langid detect library."""
        try:
            prediction = self.langid.predict(line, k=3, prob=True)
            language = prediction[0][0]
            confidence = prediction[0][1]
            return language, confidence
        
        except Exception as e:
            raise LangIDDetectionError("Language detection failed", text=line) from e