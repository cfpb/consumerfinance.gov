from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from elasticsearch_dsl import analyzer, tokenizer, token_filter

from .models import AnswerPage

label_autocomplete = analyzer(
    'label_autocomplete',
    tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=2, max_gram=25, token_chars=["letter", "digit"]),
    filter=['lowercase', token_filter('ascii_fold', 'asciifolding')]
)

synonynm_filter = token_filter(
    'synonym_filter_en',
    'synonym',
    synonyms_path = '/usr/share/elasticsearch/config/synonyms/synonyms_en.txt'
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
    portal_topics = fields.TextField()
    portal_categories = fields.TextField()
    text = fields.TextField(attr="text", analyzer=synonym_analyzer)
    url = fields.TextField()
    suggestions = fields.TextField(attr="text")
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