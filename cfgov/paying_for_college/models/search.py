from paying_for_college.documents import SchoolDocument
from search.elasticsearch_helpers import make_safe


class SchoolSearch:
    def __init__(self, search_term):
        self.search_term = make_safe(search_term).strip()
        self.results = []

    def autocomplete(self):
        s = SchoolDocument.search().query(
            'match', autocomplete=self.search_term)
        self.results = [
            {'question': result.autocomplete, 'url': result.url}
            for result in s[:20]
        ]
        return self.results

    def search(self):
        search = SchoolDocument.search().filter('term')
        if self.search_term != '':
            search = search.query('match', text=self.search_term)
        total_results = search.count()
        search = search[0:total_results]
        self.results = search.execute()[0:total_results]
        return {
            'search_term': self.search_term,
            'results': self.results
        }
