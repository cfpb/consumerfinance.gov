from django.test import TestCase
from django.test import Client

from scripts import _atomic_helpers as atomic
from v1.models.landing_page import LandingPage
from v1.models.sublanding_page import SublandingPage
from v1.models.browse_page import BrowsePage
from v1.models.browse_filterable_page import BrowseFilterablePage, EventArchivePage, NewsroomLandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage, ActivityLogPage
from v1.models.learn_page import EventPage, LearnPage, DocumentDetailPage
from v1.models.newsroom_page import NewsroomPage, LegacyNewsroomPage
from v1.models.blog_page import BlogPage, LegacyBlogPage


from helpers import publish_page


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

c = Client()

class PageTitlesTestCase(TestCase):
	""" Tests that all Wagtail page types load and display the title correctly """

	def page_loads_with_correct_title(self, page_type):
		publish_page(
			globals()[page_type](
				title = 'Title ABCD',
				slug = 'page',
			)
		)
		response = c.get('/page/')
		self.assertContains(response, 'Title ABCD')

	def test_sublanding_page(self):
		self.page_loads_with_correct_title(page_type = 'SublandingPage')

	def test_landing_page(self):
		self.page_loads_with_correct_title(page_type = 'LandingPage')

	def test_browse_page(self):
		self.page_loads_with_correct_title(page_type = 'BrowsePage')

	def test_browse_filterable_page(self):
		self.page_loads_with_correct_title(page_type = 'BrowseFilterablePage')

	def test_sublanding_filterable_page(self):
		self.page_loads_with_correct_title(page_type = 'SublandingFilterablePage')

	def test_event_archive_page(self):
		self.page_loads_with_correct_title(page_type = 'EventArchivePage')

	def test_event_page(self):
		self.page_loads_with_correct_title(page_type = 'EventPage')

	def test_learn_page(self):
		self.page_loads_with_correct_title(page_type = 'LearnPage')

	def test_document_detail_page(self):
		self.page_loads_with_correct_title(page_type = 'DocumentDetailPage')

	def test_newsroom_landing_page(self):
		self.page_loads_with_correct_title(page_type = 'NewsroomLandingPage')

	def test_newsroom_page(self):
		self.page_loads_with_correct_title(page_type = 'NewsroomPage')

	def test_legacy_newsroom_page(self):
		self.page_loads_with_correct_title(page_type = 'LegacyNewsroomPage')

	def test_legacy_blog_page(self):
		self.page_loads_with_correct_title(page_type = 'LegacyBlogPage')

	def test_blog_page(self):
		self.page_loads_with_correct_title(page_type = 'BlogPage')

	def test_activity_log_page(self):
		self.page_loads_with_correct_title(page_type = 'ActivityLogPage')

	