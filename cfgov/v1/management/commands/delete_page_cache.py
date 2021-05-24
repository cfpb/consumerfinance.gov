from django.core.management.base import BaseCommand

from wagtail.contrib.frontend_cache.utils import purge_urls_from_cache


class Command(BaseCommand):
    help = "Delete the cache of pages by full URLs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            nargs="+",
            help=(
                "The full URL for the page cache to delete "
                "(can specify multiple)"
            )
        )

    def handle(self, *args, **options):
        purge_urls_from_cache(options["url"])
