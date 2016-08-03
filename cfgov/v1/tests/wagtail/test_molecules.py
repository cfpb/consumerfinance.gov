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
		"""Quote value correctly displays on a Learn Page"""
		learn_page = LearnPage(
			title='Learn', 
			slug='learn'
		)
		learn_page.content = StreamValue(
			learn_page.content.stream_block,
			[atomic.full_width_text], 
			True
		)
		self.publish_page(child=learn_page)
		response = c.get('/learn/')
		self.assertContains(response, 'this is a quote')

	def test_call_to_action(self):
		"""Call to action value correctly displays on a Learn Page"""
		learn_page = LearnPage(
			title='Learn',
			slug='learn',
		)
		learn_page.content = StreamValue(
			learn_page.content.stream_block,
			[atomic.call_to_action],
			True
		)
		self.publish_page(child=learn_page)
		response = c.get('/learn/')
		self.assertContains(response, 'this is a call to action')

	def test_hero(self):
		"""Hero heading correctly displays on a Sublanding Filterable Page"""
		sfp = SublandingFilterablePage(
			title='Sublanding Filterable Page', 
			slug='sfp',
		)
		sfp.header = StreamValue(
			sfp.header.stream_block, 
			[atomic.hero], 
			True
		)
		self.publish_page(child=sfp)
		response = c.get('/sfp/')
		self.assertContains(response, 'this is a hero heading')


	def test_related_links(self):
		"""Related links value correctly displays on a Landing Page"""
		landing_page = LandingPage(
			title='Landing Page', 
			slug='landing', 
		)
		landing_page.sidefoot = StreamValue(
			landing_page.sidefoot.stream_block,
			[atomic.related_links], 
			True
		)
		self.publish_page(child=landing_page)
		response = c.get('/landing/')
		self.assertContains(response, 'this is a related link')

	def test_half_width_link_blob(self):
		"""Half width link blob value correctly displays on a Landing Page"""
		landing_page = LandingPage(
			title='Landing Page', 
			slug='landing', 
		)
		landing_page.content = StreamValue(
			landing_page.content.stream_block,
			[atomic.half_width_link_blob_group],
			True
		)
		self.publish_page(child=landing_page)
		response = c.get('/landing/')
		self.assertContains(response, 'this is a half width link blob')

	def test_rss_feed(self):
		"""RSS feed correctly displays on a Sublanding Page"""
		sublanding_page = SublandingPage(
			title='Sublanding Page', 
			slug='sublanding',
		)
		sublanding_page.sidefoot = StreamValue(
			sublanding_page.sidefoot.stream_block,
			[atomic.rss_feed], 
			True
		)
		self.publish_page(sublanding_page)
		response = c.get('/sublanding/')
		self.assertContains(response, 'rss-subscribe-section')

	def test_expandable(self):
		"""Expandable label value correctly displays on a Browse Page"""
		browse_page = BrowsePage(
			title='Browse Page', 
			slug='browse',
		)
		browse_page.content = StreamValue(
			browse_page.content.stream_block,
			[atomic.expandable],
			True,
		)
		self.publish_page(child=browse_page)
		response = c.get('/browse/')
		self.assertContains(response, 'this is an expandable')

	def test_related_metadata(self):
		"""Related metadata heading correctly displays on a Document Detail Page"""
		ddp = DocumentDetailPage(
			title='Document Detail Page', 
			slug='ddp',
		)
		ddp.sidefoot = StreamValue(
			ddp.sidefoot.stream_block,
			[atomic.related_metadata],
			True,
		)
		self.publish_page(child=ddp)
		response = c.get('/ddp/')
		self.assertContains(response, 'this is a related metadata heading')

	def test_image_text_50_50(self):
		"""Image Text 50 50 value correctly displays on a Landing Page"""
		landing_page = LandingPage(
			title='Landing Page', 
			slug='landing',
		)
		landing_page.content = StreamValue(
			landing_page.content.stream_block,
			[atomic.image_text_50_50_group],
			True,
		)
		self.publish_page(child=landing_page)
		response = c.get('/landing/')
		self.assertContains(response, 'this is an image text 50 50 group')
