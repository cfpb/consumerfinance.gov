from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class TestLegacyPagesRender(TestCase):
    def setUp(self):
        self.client = Client()

    def check_named_url(self, name):
        response = self.client.get(reverse(name))
        self.assertEqual(response.status_code, 200)

    def test_fellowship_page(self):
        self.check_named_url('technology_innovation_fellows')

    def test_supervision_page(self):
        self.check_named_url('jobs_supervision')
