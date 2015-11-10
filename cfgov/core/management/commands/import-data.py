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

    def handle(self, *args, **options):
        data_type = options['data_type']
        wagtail_type = options['wagtail_type'].lower()
        app = options['app']

        if not options['parent'] and not options['snippet']:
            raise CommandError('manage.py import-data: error: you must specify'
                               + ' either a parent page to import pages or'
                               + ' flag the importing as a snippet.')

        # Sheer settings: uses sheer processors to retrieve the original data.
        processors = settings.SHEER_PROCESSORS

        # Looks for the correct sheer processor to use for data retrieval.
        if data_type in processors:
            mod = import_module(processors[data_type]['processor'])
            generator = mod.documents(data_type, **processors[data_type])
            # Looks for a processor in this directory to import the module from
            # using the command line argument: wagtail_type
            try:
                module = import_module('%s.processors.%s' %
                                       (app, wagtail_type))
            except ImportError:
                raise ImportError(('No module found in %s.processors named '
                                  + '(%s)') % (app, wagtail_type))

            if 'DataImporter' in dir(module):
                importer = module.DataImporter(**options)
            else:
                importer = Importer(**options)
            try:
                converter = module.DataConverter()
            except AttributeError:
                raise AttributeError('You must define a DataConverter class.')
            for doc in generator:
                # Maps the retrieved sheer document to the given model name
                # using the imported module.
                importer.migrate(doc['_source'], converter)

            importer.print_results()
        else:
            raise CommandError('Could not find a processor for %s.'
                               % data_type)
