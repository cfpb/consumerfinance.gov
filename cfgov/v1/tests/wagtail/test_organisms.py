from django.test import TestCase
from django.test import Client


from scripts import _atomic_helpers as atomic
from v1.models.landing_page import LandingPage
from v1.models.sublanding_page import SublandingPage
from v1.models.learn_page import LearnPage
from wagtail.wagtailcore.blocks import StreamValue
from helpers import publish_page
from v1.models.snippets import Contact

c = Client()

class OrganismsTestCase(TestCase):
	def get_contact(self):
		contact = Contact(heading='Test User')
		contact.contact_info = StreamValue(
			contact.contact_info.stream_block,
			[
				atomic.contact_email,
				atomic.contact_phone,
				atomic.contact_address
			], 
			True
		)
		contact.save()
		return contact 

	def test_well(self):
		"""Well content correctly displays on a Landing Page"""
		landing_page = LandingPage(
				title='Landing Page', 
				slug='landing', 
		)
		landing_page.content = StreamValue(
			landing_page.content.stream_block, 
			[atomic.well], 
			True
		)
		publish_page(child=landing_page)
		response = c.get('/landing/')
		self.assertContains(response, 'this is well content')

	def test_main_contact_info(self):
		"""Main contact info correctly displays on a Sublanding Page"""
		sublanding_page = SublandingPage(
				title='Sublanding Page', 
				slug='sublanding', 
		)
		contact = self.get_contact()
		sublanding_page.content = StreamValue(
			sublanding_page.content.stream_block, 
			[atomic.main_contact_info(contact.id)],
			True
		)
		publish_page(child=sublanding_page)
		response = c.get('/sublanding/')
		# self.assertContains(response, 'test@example.com')
		self.assertContains(response, '(515) 123-4567')
		self.assertContains(response, '123 abc street')


	def test_sidebar_contact_info(self):
		"""Sidebar contact info correctly displays on a Landing Page"""
		landing_page = LandingPage(
				title='Landing Page', 
				slug='landing', 
		)
		contact = self.get_contact()
		landing_page.sidefoot = StreamValue(
			landing_page.sidefoot.stream_block, 
			[atomic.sidebar_contact(contact.id)],
			True
		)
		publish_page(child=landing_page)
		response = c.get('/landing/')
		# self.assertContains(response, 'test@example.com')
		self.assertContains(response, '(515) 123-4567')
		self.assertContains(response, '123 abc street')

	def test_sidebar_contact_info(self):
		"""Full width text content correctly displays on a Learn Page"""
		learn_page = LearnPage(
				title='Learn Page', 
				slug='learn', 
		)
		learn_page.content = StreamValue(
			learn_page.content.stream_block, 
			[atomic.full_width_text],
			True
		)
		publish_page(child=learn_page)
		response = c.get('/learn/')
		self.assertContains(response, 'Full width text content')


	def test_image_text_groups(self):
		"""Image Text Groups correctly display on a Landing Page"""
		landing_page = LandingPage(
			title='Landing Page', 
			slug='landing',
		)
		landing_page.content = StreamValue(
			landing_page.content.stream_block,
			[
				atomic.image_text_50_50_group,
				atomic.image_text_25_75_group
			],
			True,
		)
		publish_page(child=landing_page)
		response = c.get('/landing/')
		self.assertContains(response, 'Image 25 75 Group')
		self.assertContains(response, 'Image 50 50 Group')


	def test_half_width_link_blob_group(self):
		"""Half width link blob group correctly displays on a Landing Page"""
		landing_page = LandingPage(
			title='Landing Page', 
			slug='landing', 
		)
		landing_page.content = StreamValue(
			landing_page.content.stream_block,
			[atomic.half_width_link_blob_group],
			True
		)
		publish_page(child=landing_page)
		response = c.get('/landing/')
		self.assertContains(response, 'Half Width Link Blob Group')

	def test_email_signup(self):
		"""Email signup correctly displays on a Sublanding Page"""
		sublanding_page = SublandingPage(
			title='Sublanding Page', 
			slug='sublanding', 
		)
		sublanding_page.sidefoot = StreamValue(
			sublanding_page.sidefoot.stream_block,
			[atomic.email_signup],
			True
		)
		publish_page(child=sublanding_page)
		response = c.get('/sublanding/')
		self.assertContains(response, 'Email Sign up')
