from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter, tokenizer

from paying_for_college.models import School


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


@registry.register_document
class SchoolDocument(Document):

    autocomplete = fields.TextField(analyzer=label_autocomplete)
    text = fields.TextField(attr='settlement_school')
    nicknames = fields.TextField()
    city = fields.TextField()
    state = fields.TextField()

    def prepare_autocomplete(self, instance):
        alias_strings = [a.alias for a in instance.alias_set.all()]
        nickname_strings = [n.nickname for n in instance.nickname_set.all()]
        return alias_strings + nickname_strings

    def prepare_city(self, instance):
        return instance.city

    def prepare_nicknames(self, instance):
        return [n.nickname for n in instance.nickname_set.all()]

    def prepare_state(self, instance):
        return instance.state

    class Index:
        name = 'paying-for-college'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = School

        fields = [
            'school_id'
        ]
