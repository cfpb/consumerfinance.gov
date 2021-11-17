import os
import re
import socket
import sys
from unittest import SkipTest
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command

from wagtail.core.signals import (
    page_published, page_unpublished, post_page_move, pre_page_move
)

from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl.signals import BaseSignalProcessor
from elasticsearch_dsl import analyzer, token_filter, tokenizer

from search.models import Synonym
from v1.models.learn_page import AbstractFilterPage


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


ngram_tokenizer = analyzer(
    'ngram_tokenizer',
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
    env = settings.DEPLOY_ENVIRONMENT
    if not env or env.lower() in ('local', 'production'):
        return base_name
    else:
        return f'{env}-{base_name}'.lower()


class ElasticsearchTestsMixin:
    """Test case mixin providing useful Elasticsearch functionality.

    This test case mixin:

    - Skips all tests if running locally without Elasticsearch.
    - Makes Elasticsearch updates blocking.
    - Provides a helper method to simplify the search_index command.
    """

    @classmethod
    def setUpClass(cls):
        # If we can't connect to Elasticsearch, skip these tests, unless we are
        # running on GitHub Actions, in which case something is wrong and we
        # want the tests to fail.
        try:
            socket.create_connection((settings.ES_HOST, settings.ES_PORT))
        except OSError as e:  # pragma: nocover
            if os.getenv('GITHUB_ACTIONS'):
                raise

            raise SkipTest('Cannot connect to local Elasticsearch') from e

        # The django-elasticsearch-dsl package we use to interface with
        # Elasticsearch does not currently provide a way to make indexing
        # blocking. This test case patches the Elasticsearch bulk API call
        # to ensure that reindexes are immediately available in search results.
        #
        # See the Elasticsearch documentation on refresh:
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-refresh.html
        #
        # See https://github.com/django-es/django-elasticsearch-dsl/pull/323
        # for a proposed pull request to django-elasticsearch-dsl to support
        # this blocking behavior.
        from elasticsearch.helpers import bulk as original_bulk

        def bulk_with_refresh(*args, **kwargs):
            kwargs.setdefault('refresh', True)
            return original_bulk(*args, **kwargs)

        cls.patched_es_bulk = patch(
            'django_elasticsearch_dsl.documents.bulk',
            new=bulk_with_refresh
        )
        cls.patched_es_bulk.start()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls.patched_es_bulk.stop()

    @staticmethod
    def rebuild_elasticsearch_index(*models, stdout=sys.stdout):
        """Rebuild an Elasticsearch index, waiting for its completion.

        This method is an alias for the built-in search_index Django management
        command provided by django-elasticsearch-dsl.

        """
        call_command(
            'search_index',
            action='rebuild',
            force=True,
            models=models,
            stdout=stdout
        )


class WagtailSignalProcessor(BaseSignalProcessor):

    def handle_delete(self, sender, instance, **kwargs):
        """Handle delete.
        Given an individual model instance, delete the object from index.
        """
        # Due to the inheritance used with Filterable Lists
        # this allows us to actually delete the instance.
        if issubclass(instance.specific_class().__class__, AbstractFilterPage):
            instance_to_delete = AbstractFilterPage.objects.get(pk=instance.id)
            registry.delete(instance_to_delete, raise_on_error=False)
        else:
            registry.delete(instance, raise_on_error=False)

    def setup(self):
        # Wagtail Specific Events
        page_published.connect(self.handle_save)
        page_unpublished.connect(self.handle_delete)
        pre_page_move.connect(self.handle_delete)
        post_page_move.connect(self.handle_save)

    def teardown(self):
        # Wagtail Specific Events
        page_published.disconnect(self.handle_save)
        page_unpublished.disconnect(self.handle_delete)
        pre_page_move.disconnect(self.handle_delete)
        post_page_move.disconnect(self.handle_save)
