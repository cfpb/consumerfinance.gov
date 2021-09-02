from django.http import HttpRequest, HttpResponse
from django.test import SimpleTestCase

from core.decorators import add_headers


def view(request, *args, **kwargs):
    return HttpResponse('ok')


class AddHeadersTests(SimpleTestCase):
    def test_adds_headers(self):
        request = HttpRequest()

        response = view(request)
        self.assertNotIn('Test-Header', response)

        wrapped_view = add_headers(view, {'Test-Header': 'test'})
        response_with_headers = wrapped_view(request)
        self.assertEquals(response_with_headers['Test-Header'], 'test')
