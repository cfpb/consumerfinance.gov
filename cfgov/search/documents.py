from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter, tokenizer

from ask_cfpb.models.answer_page import AnswerPage


UNSAFE_CHARACTERS = [
    '#', '%', ';', '^', '~', '`', '|',
    '<', '>', '[', ']', '{', '}', '\\'
]


def make_safe(term):
    for char in UNSAFE_CHARACTERS:
        term = term.replace(char, '')
    return term


label_autocomplete = analyzer(
    'label_autocomplete',
    tokenizer=tokenizer(
        'trigram',
        'edge_ngram',
        min_gram=2,
        max_gram=25,
        token_chars=["letter", "digit"]
    ),
    filter=['lowercase', token_filter('ascii_fold', 'asciifolding')]
)

synonynm_filter = token_filter(
    'synonym_filter_en',
    'synonym',
    synonyms_path='/usr/share/elasticsearch/config/synonyms/synonyms_en.txt'
)

synonym_analyzer = analyzer(
    'synonym_analyzer_en',
    type='custom',
    tokenizer='standard',
    filter=[
        synonynm_filter,
        'lowercase'
    ])


@registry.register_document
class AnswerPageDocument(Document):

    autocomplete = fields.TextField(analyzer=label_autocomplete)
    portal_topics = fields.KeywordField()
    portal_categories = fields.TextField()
    text = fields.TextField(attr="text", analyzer=synonym_analyzer)
    url = fields.TextField()
    preview = fields.TextField(attr="answer_content_data")

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(live=True, redirect_to_page=None)

    def prepare_autocomplete(self, instance):
        return instance.question

    def prepare_portal_categories(self, instance):
        return [topic.heading for topic in instance.portal_category.all()]

    def prepare_portal_topics(self, instance):
        return [topic.heading for topic in instance.portal_topic.all()]

    def prepare_search_tags(self, instance):
        return instance.clean_search_tags

    def prepare_url(self, instance):
        return instance.url

    class Index:
        name = 'ask-cfpb'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = AnswerPage

        fields = [
            'search_tags',
            'language',
        ]


def get_suggestion_for_search(search_term):
    s = AnswerPageDocument.search().suggest(
        'text_suggestion', search_term, term={'field': 'text'})
    response = s.execute()
    try:
        suggested_term = response.suggest.text_suggestion[0].options[0].text
        return suggested_term
    except IndexError:
        return search_term


class AnswerPageSearch:
    def __init__(self, search_term, language='en', base_query=None):
        self.language = language
        self.search_term = make_safe(search_term).strip()
        self.base_query = base_query

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
        suggested_term = get_suggestion_for_search(self.search_term)
        if suggested_term != self.search_term:
            if not self.base_query:
                search = AnswerPageDocument.search()
            else:
                search = self.base_query
            suggested_results = search.query(
                "match", text=suggested_term).filter(
                "term", language=self.language)
            total = suggested_results.count()
            suggested_results = suggested_results[0:total]
            suggested_response = suggested_results.execute()
            results = suggested_response[0:total]
            return {
                'search_term': suggested_term,
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
