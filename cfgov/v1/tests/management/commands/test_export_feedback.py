# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from six import StringIO, ensure_text

from django.core.management import call_command
from django.test import TestCase
from django.utils.timezone import make_aware

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site

from v1.management.commands.export_feedback import parse_date
from v1.models import Feedback


class TestParseDate(TestCase):
    def test_parse_valid_date(self):
        self.assertEqual(
            parse_date('2000-01-01'),
            make_aware(datetime(2000, 1, 1, 0, 0))
        )

    def test_parse_invalid_date_raises_argumenttypeerror(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_date('foo')


class TestExportFeedback(TestCase):
    expected_csv_header = (
        '"comment","currently_own","expect_to_buy","email","is_helpful",'
        '"page","referrer","submitted_on","language"\r\n'
    )

    def setUp(self):
        root_page = Site.objects.get(is_default_site=True).root_page

        # Create three pages under the site root:
        #
        # /foo
        # /bar
        # /bar/baz
        foo_page = self.create_simple_page(root_page, 'foo')
        bar_page = self.create_simple_page(root_page, 'bar')
        baz_page = self.create_simple_page(bar_page, 'baz')

        # Create feedback for each page, for two points in time.

        # Jan 1, 2000, 11 PM
        self.first_timestamp = make_aware(datetime(2000, 1, 1, 23, 0))

        # Jan 1, 2010, 11 PM
        self.second_timestamp = make_aware(datetime(2010, 1, 1, 23, 0))

        for page in [foo_page, bar_page, baz_page]:
            for ts in (self.first_timestamp, self.second_timestamp):
                feedback = Feedback.objects.create(page=page, comment=u'ahëm')

                # This is necessary because the Feedback model uses
                # auto_now_add for the submitted_on field, which means that it
                # is always set when model instances are created, and cannot be
                # overridden.
                feedback.submitted_on = ts
                feedback.save()

    def create_simple_page(self, parent, slug):
        page = SimplePage(
            title=slug,
            slug=slug,
            content=slug,
            live=True
        )
        parent.add_child(instance=page)
        return page

    def call_command(self, *args, **kwargs):
        stdout = StringIO()
        call_command('export_feedback', *args, stdout=stdout, **kwargs)
        return ensure_text(stdout.getvalue())

    def test_export_no_feedback_header_only(self):
        Feedback.objects.all().delete()
        self.assertEqual(self.call_command(), self.expected_csv_header)

    def test_export_all_feedback(self):
        lines = self.call_command().split()
        
        # Expect one line per feedback plus the header line.
        self.assertEqual(len(lines), 7)

        # Expect that unicode characters are properly written.
        self.assertIn(
            u'"ahëm","","","","","foo","","2000-01-01",""',
            lines
        )

    def test_export_only_some_feedback(self):
        output = self.call_command('bar')

        # Expect only feedback for /bar and /baz are exported.
        self.assertEqual(len(output.split()), 5)
        self.assertNotIn('foo', output)

    def test_export_except_for_some_feedback(self):
        output = self.call_command('foo', exclude=True)

        # Expect only feedback for /bar and /baz are exported.
        self.assertEqual(len(output.split()), 5)
        self.assertNotIn('foo', output)

    def test_export_between_dates_including_start_and_end(self):
        output = self.call_command(
            from_date=self.first_timestamp,
            to_date=self.second_timestamp
        )

        # Output should contain all feedback including both dates.
        self.assertEqual(len(output.split()), 7)
