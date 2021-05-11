from django.conf import settings
from django.core.management.base import BaseCommand

from v1.models.caching import AkamaiBackend


class Command(BaseCommand):
    help = "Invalidate the cache of pages by full URLs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            nargs="+",
            help=(
                "The full URL for the page cache to invalidate "
                "(can specify multiple)"
            )
        )

    def handle(self, *args, **options):
        AkamaiBackend(
            settings.WAGTAILFRONTENDCACHE["akamai"]).purge(options["url"])
