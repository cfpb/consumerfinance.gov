from __future__ import print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks import RawHTMLBlock
from wagtail.wagtailcore.models import Site

from sheerlike.external_links import convert_http_image_links
from v1.models import LegacyBlogPage
from v1.s3utils import http_s3_url_prefix
from v1.tests.wagtail_pages.helpers import save_page


class PageValidator(object):
    def __init__(self, http_image_prefixes):
        self.http_image_prefixes = http_image_prefixes

    def validate_page(self, page, fix=False):
        valid = True

        for block in page.content:
            if not isinstance(block.block, RawHTMLBlock):
                continue

            try:
                corrected = self.correct_html(block.value)
            except Exception:
                print('failed page validation', page.full_url)
                raise

            if corrected != block.value:
                valid = False
                block.value = corrected

        if not valid:
            print('detected invalid page', page.full_url)

            if fix:
                print('saving updated page', page.full_url)
                revision = save_page(page)

                if page.live:
                    revision.publish()

    def correct_html(self, html):
        return convert_http_image_links(
            html,
            convert_url_prefixes=self.http_image_prefixes
        )


class Command(BaseCommand):
    help = 'Validates and optionally corrects raw page HTML'

    page_types_with_raw_html = (
        LegacyBlogPage,
    )

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fix', action='store_true',
                            help='correct page HTML, if possible')
        parser.add_argument('http_image_prefix', nargs='+',
                            help='HTTP image URL prefix to correct')

    def handle(self, *args, **options):
        fix = options['fix']
        http_image_prefixes = options['http_image_prefix']

        validator = PageValidator(http_image_prefixes)

        for page_type in self.page_types_with_raw_html:
            for page in page_type.objects.all():
                validator.validate_page(page, fix=fix)

    def handle_page(self, page, fix=False):
        for block in page.content:
            if not isinstance(block.block, RawHTMLBlock):
                continue

    @cached_property
    def http_image_prefixes(self):
        """Convert these HTTP image URLs to MEDIA_URL ones."""
        default_site = Site.objects.get(is_default_site=True)

        return [
            # HTTP links directly to an S3 bucket.
            # e.g. http://bucket.name/image.png
            http_s3_url_prefix(),

            # HTTP links to locally hosted Wordpress uploads.
            # e.g. http://www.mysite.com/uploads/image.png
            default_site.root_url + '/wp-content/uploads/',
        ]
