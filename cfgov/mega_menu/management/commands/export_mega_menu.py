import argparse
import json

from django.core.management.base import BaseCommand

import wagtail

from mega_menu.models import Menu


class Command(BaseCommand):
    help = 'Export mega menu content to JSON'

    def add_arguments(self, parser):
        parser.add_argument('language')
        parser.add_argument(
            'filename',
            type=argparse.FileType('w'),
            nargs='?',
            default='-'
        )

    def handle(self, *args, **options):
        menu = Menu.objects.get(language=options['language'])
        if wagtail.VERSION < (2, 12):
            data = menu.submenus.stream_data
        else:
            data = menu.submenus.raw_data
        json.dump(list(data), options['filename'], indent=4)
