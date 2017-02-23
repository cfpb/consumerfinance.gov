import os

from django.test import Client, TestCase

from helpers import publish_page, save_new_page, save_page
from v1.models.landing_page import LandingPage

django_client = Client()

class PageStatesTestCase(TestCase):

    def test_draft_page(self):
        """Draft page should not load in staging or www"""
        draft = LandingPage(
            title='Draft Page', 
            slug='draft', 
            live=False, 
            shared=False
        )
        save_new_page(child=draft)
        www_response = django_client.get('/draft/')
        self.assertEqual(www_response.status_code, 404)
        staging_response = django_client.get(
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
        save_new_page(child=shared)
        www_response = django_client.get('/shared/')
        self.assertEqual(www_response.status_code, 404)
        staging_response = django_client.get(
            '/shared/', 
            HTTP_HOST=os.environ.get('DJANGO_STAGING_HOSTNAME')
        )
        self.assertEqual(staging_response.status_code, 200)


    def test_shared_draft_page(self):
        """Shared draft page should not display unshared content"""
        shared_draft = LandingPage(
            title='Page Before Updates',
            slug='page',
            live=False,
            shared=True,
        )
        save_new_page(child=shared_draft)
        shared_draft.title = 'Draft Page Updates'
        shared_draft.shared = False
        save_page(page=shared_draft)

        www_response = django_client.get('/page/')
        self.assertEqual(www_response.status_code, 404)

        staging_response = django_client.get(
            '/page/', 
            HTTP_HOST=os.environ.get('DJANGO_STAGING_HOSTNAME')
        )
        self.assertContains(staging_response, 'Page Before Updates')
        self.assertNotContains(staging_response, 'Draft Page Updates')

    def test_live_page(self):
        """ Live page should load in www"""
        live_page = LandingPage(
            title='Live',
            slug='live',
            live=True,
        )
        publish_page(child=live_page)

        www_response = django_client.get('/live/')
        self.assertEqual(www_response.status_code, 200)


    def test_live_draft_page(self):
        """ Live draft page should not display unpublished content"""
        live_draft = LandingPage(
            title='Page Before Updates',
            slug='page',
            live=True
        )
        publish_page(child=live_draft)
        live_draft.live = False
        live_draft.title = 'Draft Page Updates'
        save_page(page=live_draft)

        www_response = django_client.get('/page/')
        self.assertContains(www_response, 'Page Before Updates')
        self.assertNotContains(www_response, 'Draft Page Updates')
