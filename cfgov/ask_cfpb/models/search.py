from haystack.query import SearchQuerySet

from flags.state import flag_enabled

from ask_cfpb.documents import AnswerPageDocument


UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term


class AnswerPageSearch:
    def __init__(self, search_term, language='en', base_query=None):
        self.language = language
        self.search_term = make_safe(search_term).strip()
        self.base_query = base_query
        self.results = []
        self.suggestion = None

    def autocomplete(self):
        s = AnswerPageDocument.search().query(
            'match', autocomplete=self.search_term)
        results = [
            {'question': result.autocomplete, 'url': result.url}
            for result in s[:20]
        ]
        return results

    def search(self):
        if not self.base_query:
            search = AnswerPageDocument.search().filter(
                "term", language=self.language)
        else:
            search = self.base_query.filter("term", language=self.language)
        if self.search_term != '':
            search = search.query("match", text=self.search_term)
        total_results = search.count()
        search = search[0:total_results]
        self.results = search.execute()[0:total_results]
        return {
            'search_term': self.search_term,
            'suggestion': self.suggestion,
            'results': self.results
        }

    def suggest(self):
        s = AnswerPageDocument.search().suggest(
            'suggestion', self.search_term, term={'field': 'text'})
        response = s.execute()
        try:
            self.suggestion = response.suggest.suggestion[0].options[0].text
        except IndexError:
            self.suggestion = self.search_term

        if self.suggestion != self.search_term:
            search = self.base_query or AnswerPageDocument.search()
            suggest_results = search.query(
                "match", text=self.suggestion).filter(
                "term", language=self.language)
            total = suggest_results.count()
            suggest_results = suggest_results[0:total]
            self.results = suggest_results.execute()[0:total]
        return {
            'search_term': self.suggestion,
            'suggestion': self.search_term,
            'results': self.results
        }


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
