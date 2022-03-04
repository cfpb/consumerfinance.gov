import argparse
import json

from django.core.management.base import BaseCommand

from mega_menu.models import Menu


class Command(BaseCommand):
    help = "Export mega menu content to JSON"

    def add_arguments(self, parser):
        parser.add_argument("language")
        parser.add_argument(
            "filename", type=argparse.FileType("w"), nargs="?", default="-"
        )

    def handle(self, *args, **options):
        menu = Menu.objects.get(language=options["language"])
        json.dump(list(menu.submenus.raw_data), options["filename"], indent=4)
