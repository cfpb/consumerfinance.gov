from django.core.management.base import BaseCommand, CommandError

from search.models import Synonym


class Command(BaseCommand):
    help = 'This command loads our synonym files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            nargs='+',
            type=str
        )

    def handle(self, *args, **options):
        for file in options['file']:
            try:
                synonym_file = open(file)
                for line in synonym_file:
                    synonym = Synonym(synonym=line.rstrip('\n'))
                    synonym.save()
            except Exception as e:
                print(e)
                raise CommandError('Failed to load synonym file %s', file)
