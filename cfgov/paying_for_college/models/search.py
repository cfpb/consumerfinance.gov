from paying_for_college.documents import SchoolDocument


UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term


class SchoolSearch:
    def __init__(self, search_term, base_query=None):
        self.search_term = make_safe(search_term).strip()
        self.base_query = base_query
        self.results = []

    def autocomplete(self):
        s = SchoolDocument.search().query(
            'match', autocomplete=self.search_term)
        results = [
            {'question': result.autocomplete, 'url': result.url}
            for result in s[:20]
        ]
        return results

    def search(self):
        if not self.base_query:
            search = SchoolDocument.search().filter("term")
        else:
            search = self.base_query.filter("term")
        if self.search_term != '':
            search = search.query("match", text=self.search_term)
        total_results = search.count()
        search = search[0:total_results]
        self.results = search.execute()[0:total_results]
        return {
            'search_term': self.search_term,
            'results': self.results
        }
