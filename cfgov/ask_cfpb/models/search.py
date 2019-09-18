from haystack.query import SearchQuerySet

from flags.state import flag_enabled


UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term


class AskSearch:
    def __init__(self, search_term, query_base=None, language='en'):
        self.query_base = query_base or SearchQuerySet().filter(
            language=language)
        self.search_term = make_safe(search_term).strip()
        self.queryset = self.query_base.filter(content=self.search_term)
        self.suggestion = None

    def suggest(self, request):
        suggestion = SearchQuerySet().spelling_suggestion(self.search_term)
        if (suggestion and suggestion != self.search_term and
                request.GET.get('correct', '1') == '1' and
                flag_enabled('ASK_SEARCH_TYPOS', request=request)):
            self.queryset = self.query_base.filter(content=suggestion)
            self.search_term, self.suggestion = suggestion, self.search_term
