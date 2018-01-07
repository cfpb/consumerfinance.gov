from django.test import TestCase

from wagtail.wagtailcore.models import Site

from v1.forms import EventArchiveFilterForm
from v1.models import CFGOVPageCategory
from v1.models.browse_filterable_page import (
    AbstractFilterPage, EventArchivePage, NewsroomLandingPage
)
from v1.tests.wagtail_pages.helpers import save_new_page


class EventArchivePageTestCase(TestCase):
    def test_get_form_class(self):
        self.assertEqual(
            EventArchivePage.get_form_class(),
            EventArchiveFilterForm
        )


class TestNewsroomLandingPage(TestCase):
    def test_no_pages_by_default(self):
        query = NewsroomLandingPage.base_query()
        self.assertFalse(query.exists())

    def test_eligible_categories(self):
        self.assertEqual(NewsroomLandingPage.eligible_categories(), [
            'at-the-cfpb',
            'data-research-reports',
            'info-for-consumers',
            'op-ed',
            'policy_compliance',
            'press-release',
            'speech',
            'testimony',
        ])

    def make_page_with_category(self, category_name):
        page = AbstractFilterPage(title='test', slug='test')
        save_new_page(page)

        category = CFGOVPageCategory.objects.create(
            name=category_name,
            page=page
        )
        page.categories.add(category)

    def test_no_pages_matching_categories(self):
        self.make_page_with_category('test')
        query = NewsroomLandingPage.base_query()
        self.assertFalse(query.exists())

    def test_page_matches_categories(self):
        self.make_page_with_category('op-ed')
        query = NewsroomLandingPage.base_query()
        self.assertTrue(query.exists())
