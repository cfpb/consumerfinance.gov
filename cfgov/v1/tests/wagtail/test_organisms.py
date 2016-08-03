from django.test import TestCase
from django.test import Client


from scripts import _atomic_helpers as atomic
from v1.models.landing_page import LandingPage
from wagtail.wagtailcore.blocks import StreamValue
from helpers import publish_page

c = Client()

class OrganismsTestCase(TestCase):
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
