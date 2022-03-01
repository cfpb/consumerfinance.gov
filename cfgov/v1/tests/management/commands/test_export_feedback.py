# -*- coding: utf-8 -*-
import argparse
import io
import tempfile
from datetime import date, datetime, timedelta
from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.utils.timezone import make_aware

from wagtail.core.models import Site
from wagtail.tests.testapp.models import SimplePage

from v1.management.commands.export_feedback import (
    lookup_page_slug,
    make_aware_datetime,
    parse_date,
)
from v1.models import Feedback


def create_simple_page(parent, slug):
    page = SimplePage(title=slug, slug=slug, content=slug, live=True)
    parent.add_child(instance=page)
    return page


class LookupPageSlug(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

    def test_lookup_valid_page_slug(self):
        self.assertEqual(lookup_page_slug(self.root_page.slug), self.root_page)

    def test_lookup_nonexistent_page_slug_raises_argumenttypeerror(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            lookup_page_slug("this-page-does-not-exist")

    def test_lookup_duplicate_page_slug_raises_argumenttypeerror(self):
        duplicate_slug = "two-pages-with-this-slug"

        page = create_simple_page(self.root_page, duplicate_slug)
        create_simple_page(page, duplicate_slug)

        with self.assertRaises(argparse.ArgumentTypeError):
            lookup_page_slug(duplicate_slug)


class TestParseDate(SimpleTestCase):
    def test_parse_valid_date(self):
        self.assertEqual(parse_date("2000-01-01"), date(2000, 1, 1))

    def test_parse_invalid_date_raises_argumenttypeerror(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_date("foo")


class TestMakeAwareDatetime(SimpleTestCase):
    def test_make_aware(self):
        self.assertEqual(
            make_aware_datetime(date(2000, 1, 1)),
            make_aware(datetime(2000, 1, 1, 0, 0, 0)),
        )


class TestExportFeedback(TestCase):
    expected_csv_header = (
        '"comment","is_helpful","page","referrer","submitted_on","language"' "\r\n"
    )

    def setUp(self):
        root_page = Site.objects.get(is_default_site=True).root_page

        # Create three pages under the site root:
        #
        # /foo
        # /bar
        # /bar/baz
        self.foo_page = create_simple_page(root_page, "foo")
        self.bar_page = create_simple_page(root_page, "bar")
        self.baz_page = create_simple_page(self.bar_page, "baz")

        # Create feedback for each page, for two points in time.

        # Jan 1, 2000, 11 PM
        self.first_timestamp = make_aware(datetime(2000, 1, 1, 23, 0))

        # Jan 1, 2010, 11 PM
        self.second_timestamp = make_aware(datetime(2010, 1, 1, 23, 0))

        for page in [self.foo_page, self.bar_page, self.baz_page]:
            for ts in (self.first_timestamp, self.second_timestamp):
                feedback = Feedback.objects.create(page=page, comment="ahëm")

                # This is necessary because the Feedback model uses
                # auto_now_add for the submitted_on field, which means that it
                # is always set when model instances are created, and cannot be
                # overridden.
                feedback.submitted_on = ts
                feedback.save()

    def call_command(self, *args, **kwargs):
        stdout = StringIO()
        call_command("export_feedback", *args, stdout=stdout, **kwargs)
        return str(stdout.getvalue())

    def test_export_no_feedback_header_only(self):
        Feedback.objects.all().delete()
        self.assertEqual(self.call_command(), self.expected_csv_header)

    def check_export_all_feedback(self, content):
        lines = content.split()

        # Expect one line per feedback plus the header line.
        self.assertEqual(len(lines), 7)

        # Expect that unicode characters are properly written.
        self.assertIn('"ahëm","","foo","","2000-01-01",""', lines)

    def test_export_all_feedback_stdout(self):
        self.check_export_all_feedback(self.call_command())

    def test_export_feedback_to_file(self):
        with tempfile.NamedTemporaryFile() as tf:
            self.call_command(filename=tf.name)

            with io.open(tf.name, encoding="utf-8") as f:
                self.check_export_all_feedback(f.read())

    def test_export_only_some_feedback(self):
        output = self.call_command(self.bar_page)

        # Expect only feedback for /bar and /baz are exported.
        self.assertEqual(len(output.split()), 5)
        self.assertNotIn("foo", output)

    def test_export_except_for_some_feedback(self):
        output = self.call_command(self.foo_page, exclude=True)

        # Expect only feedback for /bar and /baz are exported.
        self.assertEqual(len(output.split()), 5)
        self.assertNotIn("foo", output)

    def test_export_between_dates_including_start_and_end(self):
        output = self.call_command(
            from_date=self.first_timestamp.date(),
            to_date=self.second_timestamp.date(),
        )

        # Output should contain all feedback including both dates.
        self.assertEqual(len(output.split()), 7)

    def test_export_between_dates_only_some(self):
        output = self.call_command(
            from_date=self.first_timestamp.date(),
            to_date=self.first_timestamp.date() + timedelta(days=1),
        )

        # Output should contain only the first set of feedback.
        self.assertEqual(len(output.split()), 4)
        self.assertNotIn("2010", output)
