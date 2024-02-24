# interface_adapters/presenters/language_count_presenter.py
"""Module for the LanguageCountPresenter class."""

class LanguageCountPresenter:
    """Presenter to format the language counts for view."""
    def format(self, language_counts):
        """Formats the language counts for view."""
        return {lang: count for lang, count in language_counts}