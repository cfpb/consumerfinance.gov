import datetime
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from wagtail.core.models import Site

import pytz
from freezegun import freeze_time

from v1.models import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage


class InactiveUsersTestCase(TestCase):

    def setUp(self):
        self.filterable_page = BrowseFilterablePage(
            title="Blog",
            slug="test",
            live=True
        )
        self.url_path = self.filterable_page.url

        self.root = Site.objects.get(is_default_site=True).root_page
        self.root.add_child(instance=self.filterable_page)

        self.page1 = BlogPage(
            title="Page published in 2017",
            live=True,
            first_published_at=datetime.datetime(2017, 1, 1, tzinfo=pytz.UTC),
            last_published_at=datetime.datetime(2020, 1, 1, tzinfo=pytz.UTC)
        )
        self.page2 = BlogPage(
            title="Page published in 2019",
            live=True,
            first_published_at=datetime.datetime(2018, 1, 1, tzinfo=pytz.UTC),
            last_published_at=datetime.datetime(2018, 1, 1, tzinfo=pytz.UTC)
        )
        self.page3 = BlogPage(
            title="Page published in 2019",
            live=True,
            first_published_at=datetime.datetime(2019, 1, 1, tzinfo=pytz.UTC),
            last_published_at=datetime.datetime(2019, 1, 1, tzinfo=pytz.UTC)
        )
        self.page4 = BlogPage(
            title="Page in archived in 2020",
            live=True,
            is_archived="yes",
            first_published_at=datetime.datetime(2020, 1, 1, tzinfo=pytz.UTC),
            last_published_at=datetime.datetime(2020, 1, 1, tzinfo=pytz.UTC)
        )

        self.filterable_page.add_child(instance=self.page1)
        self.filterable_page.add_child(instance=self.page2)
        self.filterable_page.add_child(instance=self.page3)
        self.filterable_page.add_child(instance=self.page4)

        self.stdout = StringIO()

    def test_archive_bad_path_errors(self):
        with self.assertRaises(CommandError):
            call_command("archive_pages", "foo/bar")

    @freeze_time("2020-1-1")
    def test_archive_default_opts(self):
        call_command(
            "archive_pages",
            self.filterable_page.url,
            stdout=self.stdout,
        )

        self.page1.refresh_from_db()
        self.page2.refresh_from_db()
        self.page3.refresh_from_db()
        self.page4.refresh_from_db()

        self.assertTrue(self.page1.archived)
        self.assertFalse(self.page2.archived)
        self.assertFalse(self.page3.archived)
        self.assertTrue(self.page4.archived)

    @freeze_time("2019-2-3")
    def test_archive_months_days(self):
        call_command(
            "archive_pages",
            self.filterable_page.url,
            years=1,
            months=1,
            days=1,
            stdout=self.stdout,
        )

        self.page1.refresh_from_db()
        self.page2.refresh_from_db()
        self.page3.refresh_from_db()
        self.page4.refresh_from_db()

        self.assertTrue(self.page1.archived)
        self.assertTrue(self.page2.archived)
        self.assertFalse(self.page3.archived)
        self.assertTrue(self.page4.archived)

    @freeze_time("2020-1-2")
    def test_archive_last_publish_date(self):
        call_command(
            "archive_pages",
            self.filterable_page.url,
            years=1,
            by_published_date="last",
            stdout=self.stdout,
        )

        self.page1.refresh_from_db()
        self.page2.refresh_from_db()
        self.page3.refresh_from_db()
        self.page4.refresh_from_db()

        self.assertFalse(self.page1.archived)
        self.assertTrue(self.page2.archived)
        self.assertTrue(self.page3.archived)
        self.assertTrue(self.page4.archived)
