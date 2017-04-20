from django.core.management.base import BaseCommand, CommandError

from wagtail.contrib.wagtailfrontendcache.utils import purge_url_from_cache


class Command(BaseCommand):
    help = 'Invalidates a page by its full URL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            nargs='?',
            help='The full URL for the page you wish to invalidate'
        )

    def handle(self, *args, **options):
        page_url = options['url']
        if page_url:
            purge_url_from_cache(page_url)
        else:
            raise CommandError('Must supply a page URL')

        purge_url_from_cache(page_url)
