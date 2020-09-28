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
    def __init__(self, search_term, language='en', base_query=None,
                 document_class=None):
        self.language = language
        self.search_term = make_safe(search_term).strip()
        self.base_query = base_query
        self.document_class = document_class

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
        response = search.execute()
        results = response[0:total_results]
        return {
            'search_term': self.search_term,
            'suggestion': None,
            'results': results
        }

    def suggest(self):
        s = AnswerPageDocument.search().suggest(
            'text_suggestion', self.search_term, term={'field': 'text'})
        response = s.execute()
        try:
            suggest_term = response.suggest.text_suggestion[0].options[0].text
        except IndexError:
            suggest_term = self.search_term

        if suggest_term != self.search_term:
            if not self.base_query:
                search = AnswerPageDocument.search()
            else:
                search = self.base_query
            suggested_results = search.query(
                "match", text=suggest_term).filter(
                "term", language=self.language)
            total = suggested_results.count()
            suggested_results = suggested_results[0:total]
            suggested_response = suggested_results.execute()
            results = suggested_response[0:total]
            return {
                'search_term': suggest_term,
                'suggestion': self.search_term,
                'results': results
            }
        else:
            # We know there are no results for the original term,
            # so return an empty results list with no suggestion.
            return {
                'search_term': self.search_term,
                'suggestion': None,
                'results': []
            }
