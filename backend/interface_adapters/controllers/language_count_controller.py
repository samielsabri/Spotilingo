"""Module for the LanguageCountController class."""
class LanguageCountController:
    """Controller to count the languages of a list of songs."""
    def __init__(self, use_case, presenter):
        """Initializes the controller."""
        self.use_case = use_case
        self.presenter = presenter

    def get_language_counts(self, songs, top_n=None):
        """Gets the language counts for the given songs."""
        language_counts = self.use_case.execute(songs)
        if top_n:
            top_languages = language_counts.most_common(top_n)
        else:
            top_languages = language_counts.items()
        return self.presenter.format(top_languages)