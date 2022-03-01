# -*- coding: utf-8 -*-
import datetime
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from wagtail.core.models import Site

import pytz
from freezegun import freeze_time

from v1.models.browse_filterable_page import (
    BrowseFilterablePage,
    EventArchivePage,
)
from v1.models.learn_page import EventPage


class TestArchiveEvents(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

    def call_command(self, *args, **kwargs):
        stdout = StringIO()
        call_command("archive_events", *args, stdout=stdout, **kwargs)
        return str(stdout.getvalue())

    def test_no_events_page(self):
        with self.assertRaises(CommandError):
            self.call_command()

    def test_no_archive_page(self):
        events_page = BrowseFilterablePage(
            title="Events", slug="events", content="Events", live=True
        )
        self.root_page.add_child(instance=events_page)

        with self.assertRaises(CommandError):
            self.call_command()

    def test_no_events(self):
        events_page = BrowseFilterablePage(
            title="Events", slug="events", content="Events", live=True
        )
        self.root_page.add_child(instance=events_page)
        archive_page = EventArchivePage(
            title="Archive", slug="archive", content="archive", live=True
        )
        events_page.add_child(instance=archive_page)

        self.assertIn("No live event pages found.", self.call_command())

    @freeze_time("2020-02-02")
    def test_current_future_events_stay_in_place(self):
        events_page = BrowseFilterablePage(
            title="Events", slug="events", content="Events", live=True
        )
        self.root_page.add_child(instance=events_page)
        archive_page = EventArchivePage(
            title="Archive", slug="archive", content="archive", live=True
        )
        events_page.add_child(instance=archive_page)
        current_event_page = EventPage(
            title="Current event",
            start_dt=datetime.datetime(2020, 2, 1, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2020, 2, 2, tzinfo=pytz.UTC),
        )
        events_page.add_child(instance=current_event_page)
        future_event_page = EventPage(
            title="Future event",
            start_dt=datetime.datetime(2020, 3, 1, tzinfo=pytz.UTC),
        )
        events_page.add_child(instance=future_event_page)

        self.assertIn(
            "No past events found to be archived.", self.call_command()
        )

    @freeze_time("2020-02-02")
    def test_past_events_get_archived(self):
        events_page = BrowseFilterablePage(
            title="Events", slug="events", content="Events", live=True
        )
        self.root_page.add_child(instance=events_page)
        archive_page = EventArchivePage(
            title="Archive", slug="archive", content="archive", live=True
        )
        events_page.add_child(instance=archive_page)
        single_day_event_page = EventPage(
            title="Single-day event with implied end_dt",
            start_dt=datetime.datetime(2020, 2, 1, tzinfo=pytz.UTC),
        )
        events_page.add_child(instance=single_day_event_page)
        multi_day_event_page = EventPage(
            title="Multi-day event",
            start_dt=datetime.datetime(2020, 1, 1, tzinfo=pytz.UTC),
            end_dt=datetime.datetime(2020, 1, 2, tzinfo=pytz.UTC),
        )
        events_page.add_child(instance=multi_day_event_page)

        self.call_command()
        single_day_event_page.refresh_from_db()
        multi_day_event_page.refresh_from_db()

        self.assertEqual(single_day_event_page.parent(), archive_page)
        self.assertEqual(multi_day_event_page.parent(), archive_page)

    @freeze_time("2020-02-02")
    def test_append_date_to_duplicate_slug(self):
        events_page = BrowseFilterablePage(
            title="Events", slug="events", content="Events", live=True
        )
        self.root_page.add_child(instance=events_page)
        archive_page = EventArchivePage(
            title="Archive", slug="archive", content="archive", live=True
        )
        events_page.add_child(instance=archive_page)
        already_archived_event_page = EventPage(
            title="Already archived event page",
            slug="event",
            start_dt=datetime.datetime(2020, 1, 1, tzinfo=pytz.UTC),
        )
        archive_page.add_child(instance=already_archived_event_page)
        same_slug_event_page = EventPage(
            title="To-be-archived event page",
            slug="event",
            start_dt=datetime.datetime(2020, 1, 2, tzinfo=pytz.UTC),
        )
        events_page.add_child(instance=same_slug_event_page)

        self.call_command()
        same_slug_event_page.refresh_from_db()

        self.assertEqual(same_slug_event_page.slug, "event-2020-01-02")
