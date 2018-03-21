from __future__ import unicode_literals

from django.test import TestCase

from v1.models import BrowsePage


class ConferenceRegistrationFormTests(TestCase):
    fixtures = ['conference_registration_page.json']

    def test_page_renders_using_template(self):
        page = BrowsePage.objects.get(pk=99999)
        request = self.client.get('/').wsgi_request
        response = page.serve(request)
        self.assertContains(response, 'Which sessions will you be attending?')
