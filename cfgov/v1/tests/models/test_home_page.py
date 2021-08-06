from django.test import RequestFactory, TestCase

from v1.models import HomePage


class HomePageTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.page = HomePage(title='home', live=True)

    def check_preview_template(self, preview_mode, expected_template):
        response = self.page.serve_preview(self.request, preview_mode)
        self.assertEqual(response.template_name, expected_template)

    def test_preview_default_template(self):
        self.check_preview_template('', 'v1/home_page.html')

    def test_preview_2021_template(self):
        self.check_preview_template('home_page_2021', 'v1/home_page_2021.html')
