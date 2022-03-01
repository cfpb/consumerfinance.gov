import argparse
import json

from django.core.management.base import BaseCommand

from mega_menu.models import Menu


class Command(BaseCommand):
    help = "Import (and overwrite) language-specific mega menu content as JSON."

    def add_arguments(self, parser):
        parser.add_argument("language")
        parser.add_argument(
            "filename", type=argparse.FileType("r"), nargs="?", default="-"
        )

    def handle(self, *args, **options):
        language = options["language"]

        submenus = json.load(options["filename"])

        _, created = Menu.objects.update_or_create(
            language=language,
            defaults={
                "submenus": json.dumps(submenus),
            },
        )

        self.stdout.write(
            "%s mega menu for language %s."
            % ("Created" if created else "Updated", language)
        )
