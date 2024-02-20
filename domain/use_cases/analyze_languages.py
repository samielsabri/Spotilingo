class AnalyzeLanguages:
    def __init__(self, language_detector):
        self.language_detector = language_detector

    def execute(self, lyrics):
        return self.language_detector.detect_languages(lyrics)