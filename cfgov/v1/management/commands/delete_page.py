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
        parser.add_argument(
            '--id',
            nargs='+',
            help='The ID for the page you wish to delete'
        )

    def handle(self, *args, **options):
        page_to_delete = None
        if options['slug']:
            slug = options['slug'][0]
            try:
                page_to_delete = CFGOVPage.objects.get(slug=slug)
            except Exception as e:
                self.stderr.write(str(e))
                raise CommandError('Slug `{}` did not work'.format(slug))
        elif options['id']:
            page_id = options['id'][0]
            page_to_delete = CFGOVPage.objects.get(id=page_id)
        else:
            raise CommandError('Must supply a --slug or an --id')
        try:
            page_to_delete.unpublish()
            page_to_delete.delete()
        except Exception as e:
            self.stderr.write(str(e))
            raise CommandError('Failed to delete page {}'.format(page_to_delete))
