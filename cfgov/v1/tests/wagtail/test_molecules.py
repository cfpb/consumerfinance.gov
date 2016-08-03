import os
from django.test import TestCase
from django.test import Client

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page, Site

from scripts import _atomic_helpers as atomic
from v1.models.base import CFGOVPage
from v1.models.home_page import HomePage
from v1.models.landing_page import LandingPage
from v1.models.sublanding_page import SublandingPage
from v1.models.learn_page import EventPage, LearnPage, DocumentDetailPage
from v1.models.browse_page import BrowsePage
from v1.models.browse_filterable_page import BrowseFilterablePage, EventArchivePage, NewsroomLandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage, ActivityLogPage
from v1.models.newsroom_page import NewsroomPage, LegacyNewsroomPage
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.snippets import Contact
from wagtail.wagtailcore.blocks import StreamValue

c = Client()

class MoleculesTestCase(TestCase):

	def publish_page(self, child, root=None):
		if not root:
			root = HomePage.objects.get(title='CFGOV')
		admin_user = User.objects.get(username='admin')

		root.add_child(instance = child)
		revision = child.save_revision(
			user=admin_user,
			submitted_for_moderation=False,
		)
		revision.publish()


	def test_text_intro(self):
		"""Text introduction value correctly displays on a Browse Filterable Page"""
		bfp = BrowseFilterablePage(
			title='Browse Filterable Page', 
			slug='browse-filterable-page', 
		)
		bfp.header = StreamValue(
			bfp.header.stream_block, 
			[atomic.text_introduction], 
			True
		)
		self.publish_page(child=bfp)
		response = c.get('/browse-filterable-page/')
		self.assertContains(response, 'this is an intro')

	def test_featured_content(self):
		"""Featured content value correctly displays on a Browse Page"""
		bp = BrowsePage(
			title='Browse Page',
			slug='browse-page', 
		)
		bp.header = StreamValue(bp.header.stream_block,
		[
			atomic.featured_content
		], True)
		bp.content = StreamValue(bp.content.stream_block,
		[
			atomic.expandable,
			atomic.expandable_group
		], True)
		self.publish_page(child=bp)
		response = c.get('/browse-page/')
		self.assertContains(response, 'this is a featured content body')

	def test_quote(self):
		"""Full width text correctly displays on a Learn Page"""
		lp = LearnPage(
			title='Learn Page', 
			slug='learn-page'
		)
		lp.header = StreamValue(
			lp.header.stream_block, 
			[atomic.item_introduction], 
			True
		)
		lp.content = StreamValue(
			lp.content.stream_block,
			[
				atomic.full_width_text,
				atomic.call_to_action,
				atomic.table
			], 
			True
		)
		self.publish_page(child=lp)
		response = c.get('/learn-page/')
		self.assertContains(response, 'this is a quote')
