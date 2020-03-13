from django.core.management.base import BaseCommand

from data_research.research_conference import (
    ConferenceNotifier, get_conference_details_from_page
)


class Command(BaseCommand):
    help = 'Exports conference registration attendees via email'

    def add_arguments(self, parser):
        parser.add_argument(
            'page_id',
            type=int,
            help='ID of Wagtail page containing registration form'
        )
        parser.add_argument(
            '-f', '--from-email',
            default='donotreply@cfpb.gov',
            help='From email address (default %(default)s)'
        )
        parser.add_argument(
            '-t', '--to-email',
            required=True,
            nargs='+',
            help='To email address (may specify multiple)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Create and display email but do not send'
        )

    def handle(self, *args, **options):
        details = get_conference_details_from_page(options['page_id'])
        notifier = ConferenceNotifier(**details)

        email_message = notifier.create_email(
            from_email=options['from_email'],
            to_emails=options['to_email']
        )

        if options['verbosity']:
            self.stdout.write('To: %s' % ', '.join(email_message.to))
            self.stdout.write('From: %s' % email_message.from_email)
            self.stdout.write('Subject: %s' % email_message.subject)
            self.stdout.write(email_message.body)

        if not options['dry_run']:
            email_message.send()
