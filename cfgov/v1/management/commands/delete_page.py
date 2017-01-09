from django.core.management.base import BaseCommand, CommandError

from v1.models import CFGOVPage


class Command(BaseCommand):
    help = 'Deletes a page by its slug name'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slug',
            nargs='+',
            help='The slug for the page you wish to delete'
        )

    def handle(self, *args, **options):
        slug = options['slug'][0]
        try:
            page_to_delete = CFGOVPage.objects.get(slug=slug)
            page_to_delete.unpublish()
            page_to_delete.delete()
        except Exception as e:
            self.stderr.write(str(e))
            raise CommandError('failed to delete page {}'.format(slug))
