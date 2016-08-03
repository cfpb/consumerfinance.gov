from django.test import TestCase
from django.test import Client

from scripts import _atomic_helpers as atomic
from v1.models.landing_page import LandingPage
from helpers import publish_page, save_page

c = Client()


class PageStatesTestCase(TestCase):

	def test_draft_page(self):
		"""Draft page should not load"""
		draft = LandingPage(
			title='Draft Page', 
			slug='draft', 
			live=False, 
			shared=False
		)
		save_page(child=draft)
		response = c.get('/draft/')
		self.assertEqual(response.status_code, 404)
