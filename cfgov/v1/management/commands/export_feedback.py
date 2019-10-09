import argparse
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from wagtail.wagtailcore.models import Page

from v1.models import Feedback


def parse_date(s):
    try:
        naive_datetime = datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError('Not a valid date: %s' % s)

    return make_aware(naive_datetime)


class Command(BaseCommand):
    help = 'Export feedback submitted on the website'

    def add_arguments(self, parser):
        parser.add_argument(
            'page_slug',
            nargs='*',
            help='export only feedback for this page and its child pages'
        )
        parser.add_argument(
            '--exclude',
            action='store_true',
            help='export only feedback except for specified pages'
        )
        parser.add_argument(
            '--filename',
            type=argparse.FileType('w'),
            help='export to CSV file instead of to stdout'
        )
        parser.add_argument(
            '--from-date',
            type=parse_date,
            help='export only feedback or after this date'
        )
        parser.add_argument(
            '--to-date',
            type=parse_date,
            help='export only feedback on or before this date'
        )

    def handle(self, *args, **kwargs):
        feedbacks = Feedback.objects.for_pages(
            [Page.objects.get(slug=slug) for slug in kwargs['page_slug']],
            exclude=kwargs['exclude']
        ).order_by('submitted_on')

        if kwargs['from_date']:
            feedbacks = feedbacks.filter(submitted_on__gte=kwargs['from_date'])

        if kwargs['to_date']:
            feedbacks = feedbacks.filter(
                submitted_on__lt=kwargs['to_date'] + timedelta(days=1)
            )

        # If writing to stdout, don't append an extra newline to the CSV.
        if not kwargs['filename']:
            self.stdout.ending = ''

        feedbacks.write_csv(kwargs['filename'] or self.stdout)
