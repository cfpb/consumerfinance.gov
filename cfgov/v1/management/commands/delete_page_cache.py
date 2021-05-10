from django.core.management.base import BaseCommand

from wagtail.contrib.frontend_cache.utils import purge_url_from_cache


class Command(BaseCommand):
    help = "Delete the cache of pages by full URLs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            help="The full URLs for pages you wish to delete its cache",
        )

    def handle(self, *args, **options):
        page_urls = options["url"]
        for page_url in page_urls.split(" "):
            purge_url_from_cache(page_url)
