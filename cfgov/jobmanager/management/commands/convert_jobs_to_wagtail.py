from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from jobmanager.models import ApplicantType, ApplicantTypeSnippet


class Command(BaseCommand):
    help = 'Converts Jobmanager models to Wagtail'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--dry-run', action='store_true',
                            help='Create models but do not persist them')

    def handle(self, *args, **options):
        commit = not options['dry_run']

        self.convert_applicant_types(commit=commit)

    def convert_applicant_types(self, commit=False):
        snippets = [
            ApplicantTypeSnippet(
                applicant_type_label=at.applicant_type,
                description=at.description,
                active=at.active
            ) for at in ApplicantType.objects.all()
        ]

        count = len(snippets)
        print('converted {} ApplicantType(s)'.format(count))

        if snippets and commit:
            ApplicantTypeSnippet.objects.bulk_create(snippets)
            print('saved {} ApplicantTypeSnippet(s)'.format(count))
