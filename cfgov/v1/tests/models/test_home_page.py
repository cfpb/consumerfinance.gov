from django.test import RequestFactory, TestCase, override_settings

from v1.models.home_page import HighlightCardBlock, HomePage


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

    def test_highlight_card_block_rendering(self):
        block = HighlightCardBlock()
        value = block.to_python({
            'heading': 'Highlight',
            'text': 'This is a highlight.',
            'link_url': '/highlight/',
        })
        self.assertEqual(value.link_text, 'Read more')

    def check_render_template(self, expected_template):
        response = self.page.serve(self.request)
        self.assertEqual(response.template_name, expected_template)

    def test_render_default_template(self):
        self.check_render_template('v1/home_page.html')

    def test_render_2021_template(self):
        with override_settings(FLAGS={'HOME_PAGE_2021': [('boolean', True)]}):
            self.check_render_template('v1/home_page_2021.html')
