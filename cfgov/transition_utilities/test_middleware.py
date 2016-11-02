from django.test import TestCase
from mock import Mock
from .middleware import RewriteNemoURLsMiddleware


class RewriteNemoURLSMiddlewareTest(TestCase):

    def setUp(self):
        self.middleware = RewriteNemoURLsMiddleware()
        self.request = Mock()
        self.response = Mock()

    def test_text_transform(self):
        self.response.streaming = False
        self.response.content = "/wp-content/themes/cfpb_nemo/static.gif"
        response = self.middleware.process_response(self.request,
                                                    self.response)
        self.assertIn("/static/nemo/static.gif", response.content)
