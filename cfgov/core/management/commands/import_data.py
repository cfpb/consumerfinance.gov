from importlib import import_module

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ._helpers import Importer


class Command(BaseCommand):
    help = 'Populate a Django model using a Sheer indexer and a processor.'

    def add_arguments(self, parser):
        parser.add_argument('data_type')
        parser.add_argument('wagtail_type')
        parser.add_argument('--parent', action='store', required=False)
        parser.add_argument('--snippet', action='store_true')
        parser.add_argument('-u', '--username', action='store', required=True)
        parser.add_argument('-p', '--password', action='store', required=True)
        parser.add_argument('--app', action='store', default='v1')
        parser.add_argument('--overwrite', action='store_true')

    def get_converter(self, app, wagtail_type):
        # Looks for a processor in this directory to import the module from
        # using the command line argument: wagtail_type
        try:
            module = import_module('%s.processors.%s' %
                                   (app, wagtail_type))
        except ImportError:
            raise ImportError(('No module found in %s.processors named '
                               '(%s)') % (app, wagtail_type))
        try:
            return module.DataConverter()
        except AttributeError:
            raise AttributeError('You must define a DataConverter class.')

    def get_processor(self, data_type, processors):
        # Looks for the correct sheer processor to use for data retrieval.
        if data_type not in processors:
            raise CommandError('Could not find a processor for %s.'
                               % data_type)
        return import_module(processors[data_type]['processor'])

    def get_documents(self, data_type, processors):
        processor = self.get_processor(data_type, processors)
        # 'name' is actually an unused param, so we just pass None for now
        return processor.documents(name=None,
                                   url=processors[data_type]['url'])

    def handle(self, *args, **options):
        if not options['parent'] and not options['snippet']:
            raise CommandError('manage.py import-data: error: you must '
                               'specify either a parent page to import '
                               'pages or flag the importing as a snippet.')

        documents = self.get_documents(options['data_type'],
                                       settings.SHEER_PROCESSORS)
        importer = Importer(**options)
        converter = self.get_converter(options['app'],
                                       options['wagtail_type'].lower())

        for doc in documents:
            # Maps the retrieved sheer document to the given model name
            # using the imported module.
            importer.migrate(doc['_source'], converter)

        importer.print_results()
