"""This module contains the FastTextDetector class, which is an implementation of the ILanguageDetector interface."""
import fasttext
from .language_detector import ILanguageDetector

class FastTextDetectionError(Exception):
    """Custom exception for FastText detection errors."""
    def __init__(self, message, text=None):
        super().__init__(message)
        self.message = message
        self.text = text

    def __str__(self):
        """
        String representation of the error, including the text if available.
        """
        if self.text:
            return f"FastTextDetectionError: {self.message} | Text: {self.text}"
        return f"FastTextDetectionError: {self.message}"


class FastTextDetector(ILanguageDetector):
    """FastText language detector."""
    def __init__(self, model_path):
        """Initializes the FastText language detector."""
        try:
            fasttext.FastText.eprint = lambda x: None 
            self.model = fasttext.load_model(model_path)
        except Exception as e:
            raise FastTextDetectionError(f"Failed to load FastText model: {str(e)}") from e

    def detect_languages(self, line):
        """Detects the language of the given text using Fasttext Model."""
        try:
            prediction = self.model.predict(line, k=3)
            language = prediction[0][0].replace('__label__', '')
            confidence = prediction[1][0]
            return language, confidence
        
        except Exception as e:
            raise FastTextDetectionError("Language detection failed", text=line) from e