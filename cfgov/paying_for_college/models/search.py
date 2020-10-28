from paying_for_college.documents import SchoolDocument
from search.elasticsearch_helpers import make_safe


class SchoolSearch:
    def __init__(self, search_term):
        self.search_term = make_safe(search_term).strip()
        self.results = []

    def autocomplete(self):
        if self.search_term != '':
            search = SchoolDocument.search().query(
                'match', autocomplete=self.search_term)
            self.results = search.execute()
        return {
            'search_term': self.search_term,
            'results': self.results
        }
