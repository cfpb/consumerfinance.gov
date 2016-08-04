from __future__ import absolute_import, print_function

import requests

from django.core.management.base import BaseCommand, CommandError
from urlparse import urljoin, urlparse

from core.pdf import PDFGenerator


class Command(BaseCommand):
    help = 'Generate a PDF from a webpage'

    def add_arguments(self, parser):
        parser.add_argument('url', help='source URL')
        parser.add_argument('filename', help='destination filename')

    def handle(self, *args, **options):
        url = options['url']
        filename = options['filename']

        parts = urlparse(url)
        base_url = '{}://{}/'.format(parts.scheme, parts.netloc)
        print('using base URL {}'.format(base_url))

        generator = PDFGenerator(base_url)
        if not generator.enabled:
            raise CommandError(
                'PDF generation disabled, nothing to do.\n'
                '(Do you have PDFREACTOR_LIB and PDFREACTOR_LICENSE defined?)'
            )

        html = requests.get(url).text
        pdf = generator.generate_pdf(html)

        with open(filename, 'wb') as f:
            f.write(pdf)
