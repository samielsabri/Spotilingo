import fasttext

class FastTextDetector:
    def __init__(self, model_path):
        self.model = fasttext.load_model(model_path)

    def detect_languages(self, lyrics):
        # Your implementation to detect languages using FastText
        pass