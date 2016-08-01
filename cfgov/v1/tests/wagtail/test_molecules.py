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

	@classmethod
	def setUpClass(cls):
		super(MoleculesTestCase, cls).setUpClass()
		admin_user = User(
			username='admin',
			password=make_password(os.environ.get('WAGTAIL_ADMIN_PW')),
			is_superuser=True, is_active=True, is_staff=True
		)
		admin_user.save()
		cls.admin_user = admin_user
		root = Page.objects.first()
		site_root = HomePage(
			title='CFGOV', slug='home-page', depth=2, owner=admin_user
		)
		site_root.live = True
		root.add_child(instance=site_root)
		latest = site_root.save_revision(
			user=admin_user, submitted_for_moderation=False
		)
		latest.save()
		cls.site_root = site_root

		# Setting new site root
		site = Site.objects.first()
		site.port = 8000
		site.root_page_id = site_root.id
		site.save()
		content_site = Site(
			hostname='content.localhost', port=8000, root_page_id=site_root.id
		)
		content_site.save()

	@classmethod
	def publish_page(cls, child):
		cls.site_root.add_child(instance=child)
		revision = child.save_revision(
			user=cls.admin_user,
			submitted_for_moderation=False,
		)
		revision.publish()


	def test_text_intro(self):
		"""Text introduction value correctly displays on a Browse Filterable Page"""
		bfp = BrowseFilterablePage(
			title='Browse Filterable Page', 
			slug='browse-filterable-page', 
			owner=self.admin_user
		)
		bfp.header = StreamValue(
			bfp.header.stream_block, 
			[atomic.text_introduction], 
			True
		)
		self.publish_page(child=bfp)
		response = c.get('/browse-filterable-page/')
		self.assertContains(response, 'this is an intro')

	# def test_featured_content(self):
	# 	"""Featured content value correctly displays on a Browse Page"""
	# 	bp = BrowsePage(
	# 		title='Browse Page',
	# 		slug='browse-page', 
	# 		owner=self.admin_user
	# 	)
	# 	bp.header = StreamValue(bp.header.stream_block,
	# 	[
	# 		atomic.featured_content
	# 	], True)
	# 	bp.content = StreamValue(bp.content.stream_block,
	# 	[
	# 		atomic.expandable,
	# 		atomic.expandable_group
	# 	], True)
	# 	self.publish_page(bp)
	# 	response = c.get('/browse-page/')
	# 	self.assertContains(response, 'this is a featured content body')
