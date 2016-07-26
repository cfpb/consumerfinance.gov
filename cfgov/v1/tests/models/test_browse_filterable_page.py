from unittest import TestCase

from v1.forms import EventArchiveFilterForm, NewsroomFilterForm
from v1.models.browse_filterable_page import (
    EventArchivePage, NewsroomLandingPage
)


class EventArchivePageTestCase(TestCase):
    def test_get_form_class(self):
        self.assertEqual(
            EventArchivePage.get_form_class(),
            EventArchiveFilterForm
        )


class NewroomLandingPageTestCase(TestCase):
    def test_get_form_class(self):
        self.assertEqual(
            NewsroomLandingPage.get_form_class(),
            NewsroomFilterForm
        )
