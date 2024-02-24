# interface_adapters/presenters/language_count_presenter.py
"""Module for the LanguageCountPresenter class."""

class LanguageCountPresenter:
    """Presenter to format the language counts for view."""
    def format(self, language_counts):
        """Formats the language counts for view."""
        sorted_language_counts = dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True))
        return sorted_language_counts