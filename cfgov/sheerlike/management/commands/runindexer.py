import sys
import os.path
import codecs
import json

from importlib import import_module 

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from unipath import Path

class Command(BaseCommand):
    help = "populate a Django model using a Sheer indexer"


    def add_arguments(self,parser):
        parser.add_argument('indexer_name')
        parser.add_argument('target_model')

    def handle(self, *args, **options):
        indexer_name = options ['indexer_name']

        sheer_sites = settings.SHEER_SITES
        sheer_libs = [Path(s).child('_lib') for s in sheer_sites]
        sys.path += sheer_libs

        processors = {}
        
        possible_processor_configs =\
        [Path(s).child('_settings').child('processors.json') for s in sheer_sites]

        for procjson in possible_processor_configs:
            if os.path.exists(procjson):
                with codecs.open(procjson, encoding='utf8') as jsonfile:
                    raw_json = jsonfile.read()
                    merged_json = os.path.expandvars(raw_json)
                    config = json.loads(merged_json)
                    processors.update(config)
                    
        if indexer_name in processors:
            mod = import_module(processors[indexer_name]['processor'])
            generator = mod.documents(indexer_name, **processors[indexer_name])

            for doc in generator:
                self.stdout.write(str(doc))

        else:
            raise CommandError('could not find a processor for %s' % indexer_name)
