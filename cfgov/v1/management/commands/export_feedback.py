import argparse
import io
from datetime import datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from wagtail.core.models import Page

from v1.models import Feedback


def lookup_page_slug(s):
    try:
        return Page.objects.get(slug=s)
    except Page.DoesNotExist:
        raise argparse.ArgumentTypeError('No page with slug: %s' % s)
    except Page.MultipleObjectsReturned:
        raise argparse.ArgumentTypeError('Multiple pages with slug: %s' % s)


def parse_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError('Not a valid date: %s' % s)


def make_aware_datetime(date):
    return make_aware(datetime.combine(date, time()))


class Command(BaseCommand):
    help = 'Export feedback submitted on the website'

    def add_arguments(self, parser):
        parser.add_argument(
            'pages',
            nargs='*',
            type=lookup_page_slug,
            help=(
                'export only feedback for these page slugs '
                'and their child pages'
            )
        )
        parser.add_argument(
            '--exclude',
            action='store_true',
            help='export only feedback except for specified pages'
        )
        parser.add_argument(
            '--filename',
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
            kwargs['pages'],
            exclude=kwargs['exclude']
        ).order_by('submitted_on')

        if kwargs['from_date']:
            feedbacks = feedbacks.filter(
                submitted_on__gte=make_aware_datetime(kwargs['from_date'])
            )

        if kwargs['to_date']:
            feedbacks = feedbacks.filter(submitted_on__lt=(
                make_aware_datetime(kwargs['to_date']) + timedelta(days=1)
            ))

        if kwargs['filename']:
            with io.open(
                kwargs['filename'],
                mode='w',
                newline='',
                encoding='utf-8'
            ) as f:
                feedbacks.write_csv(f)
        else:
            # If writing to stdout, don't append an extra newline to the CSV.
            self.stdout.ending = ''

            feedbacks.write_csv(self.stdout)
