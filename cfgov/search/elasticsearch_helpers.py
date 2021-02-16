import re

from django.conf import settings

from elasticsearch_dsl import analyzer, token_filter, tokenizer
from unittest.mock import patch

from search.models import Synonym


def strip_html(markup):
    """
    Make sure markup stripping doesn't mash content elements together.

    Also remove no-break space characters.
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, " ", markup).strip().replace("\xa0", "")


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


def get_synonyms():
    try:
        return list(Synonym.objects.values_list('synonym', flat=True))
    except Exception:
        return []


synonym_filter = token_filter(
    'synonym_filter',
    'synonym',
    synonyms=get_synonyms()
)

synonym_analyzer = analyzer(
    'synonym_analyzer',
    type='custom',
    tokenizer='standard',
    filter=[
        synonym_filter,
        'lowercase'
    ])


def environment_specific_index(base_name):
    if settings.DEPLOY_ENVIRONMENT in (None, '', 'local', 'production'):
        return base_name
    else:
        return f'{settings.DEPLOY_ENVIRONMENT}-{base_name}'


# https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-refresh.html
class WaitForElasticsearchMixin:
    """Test case mixin that makes Elasticsearch bulk updates blocking."""
    @classmethod
    def setUpClass(cls):
        from elasticsearch.helpers import bulk as original_bulk

        def bulk_wait_for_refresh(*args, **kwargs):
            kwargs.setdefault('refresh', 'wait_for')
            return original_bulk(*args, **kwargs)

        cls.patched_es_bulk = patch(
            'django_elasticsearch_dsl.documents.bulk',
            new=bulk_wait_for_refresh
        )
        cls.patched_es_bulk.start()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.patched_es_bulk.stop()

        super().tearDownClass()
