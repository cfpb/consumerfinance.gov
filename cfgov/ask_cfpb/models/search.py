from elasticsearch7.exceptions import RequestError

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
        try:
            s = AnswerPageDocument.search().filter(
                "term", language=self.language
            ).query(
                'match', autocomplete=self.search_term
            )
            results = [
                {'question': result.autocomplete, 'url': result.url}
                for result in s[:20]
            ]
        except RequestError:
            results = []
        return results

    def search(self):
        if not self.base_query:
            search = AnswerPageDocument.search().filter(
                "term", language=self.language)
        else:
            search = self.base_query.filter("term", language=self.language)
        if self.search_term != '':
            search = search.query(
                "match", text={"query": self.search_term, "operator": "AND"}
            )
        total_results = search.count()
        search = search[0:total_results]
        self.results = search.execute()[0:total_results]
        return {
            'search_term': self.search_term,
            'suggestion': self.suggestion,
            'results': self.results
        }

    def suggest(self):
        s = AnswerPageDocument.search().filter(
            "term", language=self.language).suggest(
            'suggestion', self.search_term, term={'field': 'text'})
        response = s.execute()
        try:
            self.suggestion = response.suggest.suggestion[0].options[0].text
        except IndexError:
            # No Suggestions Found
            return {
                'search_term': self.search_term,
                'suggestion': None,
                'results': self.results
            }

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
