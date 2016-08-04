from django.test import TestCase
from django.test import Client

from scripts import _atomic_helpers as atomic
from v1.models.landing_page import LandingPage
from helpers import publish_page, save_page
import os

c = Client()

class PageStatesTestCase(TestCase):

	def test_draft_page(self):
		"""Draft page should not load in staging or www"""
		draft = LandingPage(
			title='Draft Page', 
			slug='draft', 
			live=False, 
			shared=False
		)
		save_page(child=draft)
		www_response = c.get('/draft/')
		self.assertEqual(www_response.status_code, 404)
		staging_response = c.get(
			'/draft/', 
			HTTP_HOST=os.environ.get('DJANGO_STAGING_HOSTNAME')
		)
		self.assertEqual(staging_response.status_code, 404)

	def test_shared_page(self):
		"""Shared page should load in staging but not www"""
		shared = LandingPage(
			title='Landing Page',
			slug='shared',
			live=False,
			shared=True,
		)
		save_page(child=shared)
		www_response = c.get('/shared/')
		self.assertEqual(www_response.status_code, 404)
		staging_response = c.get(
			'/shared/', 
			HTTP_HOST=os.environ.get('DJANGO_STAGING_HOSTNAME')
		)
		self.assertEqual(staging_response.status_code, 200)

