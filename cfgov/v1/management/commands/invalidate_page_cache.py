from django.core.management.base import BaseCommand

from wagtail.contrib.frontend_cache.utils import PurgeBatch


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
        batch = PurgeBatch()
        batch.add_urls(options["url"])
        batch.purge()
