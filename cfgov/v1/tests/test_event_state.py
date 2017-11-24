import datetime
from datetime import timedelta

from django.test import TestCase

from pytz import timezone

from sheerlike.query import when


class TestEventState(TestCase):

    def test_past_event(self):
        event_end = datetime.datetime.now(timezone('America/New_York')) - timedelta(minutes = 5)
        event_start = event_end - timedelta(hours = 1)
        self.assertEquals(when(event_start, event_end), 'past')

    def test_future_event(self):
        event_start = datetime.datetime.now(timezone('America/New_York')) + timedelta(minutes = 5)
        event_end = event_start + timedelta(hours = 1)
        self.assertEquals(when(event_start, event_end), 'future')

    def test_present_event(self):
        event_start = datetime.datetime.now(timezone('America/New_York')) - timedelta(minutes = 5)
        event_end = event_start + timedelta(hours = 1)
        self.assertEquals(when(event_start, event_end), 'present')
