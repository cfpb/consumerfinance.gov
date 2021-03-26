from django.core.management.base import BaseCommand

from housing_counselor.generator import generate_counselor_html


class Command(BaseCommand):
    help = 'Generate bulk housing counselor HTML data'

    def add_arguments(self, parser):
        parser.add_argument('source')
        parser.add_argument('target')

    def handle(self, *args, **options):
        generate_counselor_html(options['source'], options['target'])
