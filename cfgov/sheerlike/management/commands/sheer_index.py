import os.path

from django.conf import settings
from django.core.management.base import BaseCommand

from sheerlike.indexer import index


LOCATION = os.environ.get('SHEER_LOCATION', os.getcwd())
ELASTICSEARCH_HOSTS = settings.SHEER_ELASTICSEARCH_SERVER
ELASTICSEARCH_INDEX = settings.SHEER_ELASTICSEARCH_INDEX


class Command(BaseCommand):
    help = "Run the classic 'sheer' indexer"

    def add_arguments(self, parser):
        parser.add_argument('--reindex', '-r', action="store_true",
                            help="Recreate the index and reindex all content.")
        parser.add_argument('--processors', '-p', nargs='*',
                            help='Content processors to index.')

        parser.add_argument(
            '--elasticsearch',
            '-e',
            default=ELASTICSEARCH_HOSTS,
            help=("Elasticsearch host:port pairs. Separate hosts with commas. "
                  "Default is localhost:9200. You can also set the "
                  "SHEER_ELASTICSEARCH_HOSTS environment variable."))
        parser.add_argument(
            '--index',
            '-i',
            default=ELASTICSEARCH_INDEX,
            help=("Elasticsearch index name. Default is 'content'. You can "
                  "also set the SHEER_ELASTICSEARCH_INDEX environment "
                  "variable."))

    def handle(self, *args, **options):
        index(args, options)
