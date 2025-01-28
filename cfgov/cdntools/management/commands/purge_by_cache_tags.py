from django.core.management.base import BaseCommand

from wagtail.contrib.frontend_cache.utils import get_backends


class Command(BaseCommand):
    help = "Invalidate the cache of pages by cache tag"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cache_tag",
            required=True,
            nargs="+",
            help=("The cache tag to invalidate (can specify multiple)"),
        )
        parser.add_argument(
            "--action",
            type=str,
            default="invalidate",
            help=(
                "Purge cache by tag using either the "
                "'invalidate' or 'delete' action. Default: invalidate"
            ),
        )

    def handle(self, *args, **options):
        cache_tags = options["cache_tag"]
        action = options["action"]
        akamai_backend = get_backends(backends="akamai")["akamai"]
        akamai_backend.purge_by_tags(cache_tags, action=action)
