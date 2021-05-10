import re

from django.core.management.base import BaseCommand

from wagtail.contrib.frontend_cache.utils import purge_url_from_cache


class Command(BaseCommand):
    help = "Invalidate the cache of pages by full URLs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            help="The full URLs for pages you wish to invalidate its cache",
        )

    def handle(self, *args, **options):
        page_urls = options["url"]
        if re.search(r"\s", page_urls):
            for page_url in page_urls:
                purge_url_from_cache(page_url)
        else:
            purge_url_from_cache(page_urls)
