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
        synonyms_saved = 0
        for file in options['file']:
            try:
                synonym_file = open(file)
                for line in synonym_file:
                    synonym = Synonym(synonym=line.rstrip('\n'))
                    synonym.save()
                    synonyms_saved += 1
            except Exception:
                raise CommandError('Failed to load synonym file %s', file)
        self.stdout.write(f'Successfully saved {synonyms_saved} synonyms')
