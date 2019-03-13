from django.test import Client, TestCase

from scripts import _atomic_helpers as atomic

from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.browse_filterable_page import (
    BrowseFilterablePage, EventArchivePage, NewsroomLandingPage
)
from v1.models.browse_page import BrowsePage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import DocumentDetailPage, EventPage, LearnPage
from v1.models.newsroom_page import LegacyNewsroomPage, NewsroomPage
from v1.models.sublanding_filterable_page import (
    ActivityLogPage, SublandingFilterablePage
)
from v1.models.sublanding_page import SublandingPage
from v1.tests.wagtail_pages.helpers import publish_page


'''
Page types tested here:

LandingPage,
SubLandingPage,
BrowsePage,
BrowseFilterablePage,
SublandingFilterablePage,
EventArchivePage,
DocumentDetailPage,
LearnPage,
EventPage,
NewsroomLandingPage,
NewsroomPage,
LegacyNewsroomPage,
BlogPage,
LegacyBlogPage,
ActivityLogPage

'''

django_client = Client()

class PageTitlesTestCase(TestCase):
    """ Tests that all Wagtail page types load and display the title correctly """

    def page_loads_with_correct_title(self, page_cls):
        publish_page(
            page_cls(
                title = 'Title ABCD',
                slug = 'page',
            )
        )
        response = django_client.get('/page/')
        self.assertContains(response, 'Title ABCD')

    def test_sublanding_page(self):
        self.page_loads_with_correct_title(page_cls=SublandingPage)

    def test_landing_page(self):
        self.page_loads_with_correct_title(page_cls=LandingPage)

    def test_browse_page(self):
        self.page_loads_with_correct_title(page_cls=BrowsePage)

    def test_browse_filterable_page(self):
        self.page_loads_with_correct_title(page_cls=BrowseFilterablePage)

    def test_sublanding_filterable_page(self):
        self.page_loads_with_correct_title(page_cls=SublandingFilterablePage)

    def test_event_archive_page(self):
        self.page_loads_with_correct_title(page_cls=EventArchivePage)

    def test_event_page(self):
        self.page_loads_with_correct_title(page_cls=EventPage)

    def test_learn_page(self):
        self.page_loads_with_correct_title(page_cls=LearnPage)

    def test_document_detail_page(self):
        self.page_loads_with_correct_title(page_cls=DocumentDetailPage)

    def test_newsroom_landing_page(self):
        self.page_loads_with_correct_title(page_cls=NewsroomLandingPage)

    def test_newsroom_page(self):
        self.page_loads_with_correct_title(page_cls=NewsroomPage)

    def test_legacy_newsroom_page(self):
        self.page_loads_with_correct_title(page_cls=LegacyNewsroomPage)

    def test_legacy_blog_page(self):
        self.page_loads_with_correct_title(page_cls=LegacyBlogPage)

    def test_blog_page(self):
        self.page_loads_with_correct_title(page_cls=BlogPage)

    def test_activity_log_page(self):
        self.page_loads_with_correct_title(page_cls=ActivityLogPage)
