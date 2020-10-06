UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term


# class DocumentPageSearch:
#     def __init__(self, search_term, language='en', base_query=None,
#                  document_class=None):
#         self.language = language
#         self.search_term = make_safe(search_term).strip()
#         self.base_query = base_query
#         self.document_class = document_class
#         self.results = []
#         self.suggestion = None

#     def autocomplete(self):
#         s = self.document_class.search().query(
#             'match', autocomplete=self.search_term)
#         results = [
#             {'question': result.autocomplete, 'url': result.url}
#             for result in s[:20]
#         ]
#         return results

#     def search(self):
#         if not self.base_query:
#             search = self.document_class.search().filter(
#                 "term", language=self.language)
#         else:
#             search = self.base_query.filter("term", language=self.language)
#         if self.search_term != '':
#             search = search.query("match", text=self.search_term)
#         total_results = search.count()
#         search = search[0:total_results]
#         self.results = search.execute()[0:total_results]
#         return {
#             'search_term': self.search_term,
#             'suggestion': self.suggestion,
#             'results': self.results
#         }

#     def suggest(self):
#         s = self.document_class.search().suggest(
#             'text_suggestion', self.search_term, term={'field': 'text'})
#         response = s.execute()
#         try:
#             suggestion = response.suggest.text_suggestion[0].options[0].text
#         except IndexError:
#             suggestion = self.search_term

#         if suggestion != self.search_term:
#             search = self.base_query or self.document_class.search()
#             suggest_results = search.query(
#                 "match", text=suggestion).filter(
#                 "term", language=self.language)
#             total = suggest_results.count()
#             suggest_results = suggest_results[0:total]
#             self.results = suggest_results.execute()[0:total]
#             return {
#                 'search_term': suggestion,
#                 'suggestion': self.search_term,
#                 'results': self.results
#             }
#         else:
#             # We know there are no results for the original term,
#             # so return an empty results list with no suggestion.
#             return {
#                 'search_term': self.search_term,
#                 'suggestion': self.suggestion,
#                 'results': self.results
#             }
