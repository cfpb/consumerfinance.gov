from django.core.management.base import BaseCommand
from wagtail.wagtailcore.blocks import RawHTMLBlock

from sheerlike.external_links import convert_http_image_links
from v1.models import LegacyBlogPage


class Command(BaseCommand):
    help = 'Validates and optionally corrects raw page HTML'

    page_types_with_raw_html = (
        LegacyBlogPage,
    )

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fix', action='store_true',
                            help='correct page HTML, if possible')

    def handle(self, *args, **options):
        for page_type in self.page_types_with_raw_html:
            for page in page_type.objects.all():
                self.handle_page(page)

    def handle_page(self, page):
        for block in page.content:
            if not isinstance(block.block, RawHTMLBlock):
                continue

            corrected = convert_http_image_links(block.value)

            if corrected != block.value:
                print('made a change')
