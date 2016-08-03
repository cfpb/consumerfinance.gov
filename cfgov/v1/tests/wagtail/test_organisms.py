from django.test import TestCase
from django.test import Client


from scripts import _atomic_helpers as atomic
from v1.models.landing_page import LandingPage
from v1.models.sublanding_page import SublandingPage
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
		self.assertContains(response, 'test@example.com')
		self.assertContains(response, '(515) 123-4567')
		self.assertContains(response, '123 abc street')


