from django.core.management.base import BaseCommand, CommandError

from v1.models import LegacyBlogPage
from v1.page_validation import PageValidator


class Command(BaseCommand):
    help = "Validates and optionally corrects raw page HTML"

    page_types_with_raw_html = (LegacyBlogPage,)

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--fix",
            action="store_true",
            help="correct page HTML, if possible",
        )
        parser.add_argument(
            "http_image_url_mapping",
            nargs="+",
            help=(
                "HTTP image URL mapping to correct, "
                "e.g. http://from.url/,http://to.url/"
            ),
        )

    def handle(self, *args, **options):
        fix = options["fix"]
        http_image_url_mappings = [
            tuple(mapping.split(",")) for mapping in options["http_image_url_mapping"]
        ]

        for mapping in http_image_url_mappings:
            if 2 != len(mapping):
                raise CommandError(
                    "HTTP image URL mappings must be comma-separated pairs"
                )

        print("using these HTTP image URL mappings:")
        for mapping in http_image_url_mappings:
            print("{} -> {}".format(*mapping))

        validator = PageValidator(http_image_url_mappings)

        for page_type in self.page_types_with_raw_html:
            for page in page_type.objects.all():
                validator.validate_page(page, fix=fix)
