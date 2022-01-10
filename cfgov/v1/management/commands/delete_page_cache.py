
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

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
        # Get the default frontend cache settings
        global_settings = getattr(settings, 'WAGTAILFRONTENDCACHE', {})

        # If Akamai isn't configured, we can't do anything anyway
        if "akamai" not in global_settings:
            raise CommandError("Akamai is not configured")

        # Create settings specific to our deletion backend
        delete_settings = {"akamai_deleting": {
            "BACKEND": "v1.models.caching.AkamaiDeletingBackend",
            "CLIENT_TOKEN": global_settings["akamai"]["CLIENT_TOKEN"],
            "CLIENT_SECRET": global_settings["akamai"]["CLIENT_SECRET"],
            "ACCESS_TOKEN": global_settings["akamai"]["ACCESS_TOKEN"],
        }}

        # Purge using the deleting backend
        purge_urls_from_cache(
            options["url"],
            backend_settings=delete_settings,
            backends=["akamai_deleting"]
        )
