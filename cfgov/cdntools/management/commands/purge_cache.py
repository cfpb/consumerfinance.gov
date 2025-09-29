import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from wagtail.contrib.frontend_cache.utils import PurgeBatch, get_backends


class Command(BaseCommand):
    help = "Perorm invalidation purges of the frontend cache"

    def add_arguments(self, parser):
        parser.add_argument(
            "--backend",
            nargs="+",
            help="Limit the purge the given frontend cache backend name",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Purge all URLs for all backends. ",
        )
        parser.add_argument(
            "--cache_tag",
            nargs="+",
            help="The cache tag to invalidate (can specify multiple). ",
        )
        parser.add_argument(
            "--url",
            nargs="+",
            help=(
                "The full URL for the page cache to invalidate "
                "(can specify multiple)."
            ),
        )

    def handle(self, *args, **options):
        backends = options["backend"]
        all = options["all"]
        urls = options["url"]
        cache_tags = options["cache_tag"]

        if backends is not None:
            self.validate_backends(backends)

        if not any((all, urls, cache_tags)):
            self.stderr.write(
                self.style.ERROR(
                    "Please provide one or more of --all/--url/--cache_tag"
                )
            )

        if all:
            self.handle_all(backends=backends)

        if urls is not None:
            self.handle_urls(urls, backends=backends)

        if cache_tags is not None:
            self.handle_cache_tags(cache_tags, backends=backends)

    def validate_backends(self, backends):
        backend_settings = getattr(settings, "WAGTAILFRONTENDCACHE", {})
        missing_backends = set(backends) - set(backend_settings.keys())
        if len(missing_backends) > 0:
            self.stderr.write(
                self.style.ERROR(
                    "Frontend cache backends are not configured: "
                    f"{','.join(missing_backends)}"
                )
            )
            sys.exit(1)

    def handle_urls(self, urls, backends=None):
        batch = PurgeBatch()
        batch.add_urls(urls)
        batch.purge(backends=backends)

    def handle_cache_tags(self, tags, backends=None):
        for name, backend in get_backends(backends=backends).items():
            # Cache tags can only be purged by an AkamaiBackend
            try:
                backend.purge_by_tags(tags)
            except AttributeError:
                self.stderr.write(
                    self.style.ERROR(f"Cannot purge tags from backend: {name}")
                )

    def handle_all(self, backends=None):
        for name, backend in get_backends(backends=backends).items():
            # An entire site can only be purged on an AkamaiBackend
            try:
                backend.purge_all()
            except AttributeError:
                self.stderr.write(
                    self.style.ERROR(f"Cannot purge all from backend: {name}")
                )
