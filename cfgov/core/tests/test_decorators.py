from django.http import HttpRequest, HttpResponse
from django.test import SimpleTestCase

from core.decorators import add_headers, akamai_no_store


def view(request, *args, **kwargs):
    return HttpResponse('ok')


@akamai_no_store
def view_no_store(request, *args, **kwargs):
    return HttpResponse('no store')


class DecoratorTests(SimpleTestCase):
    def setUp(self):
        self.request = HttpRequest()

    def test_adds_headers(self):
        response = view(self.request)
        self.assertNotIn('Test-Header', response)

        wrapped_view = add_headers(view, {'Test-Header': 'test'})
        response_with_headers = wrapped_view(self.request)
        self.assertEquals(response_with_headers['Test-Header'], 'test')

    def test_akamai_no_store(self):
        response = view_no_store(self.request)
        self.assertEquals(response['Edge-Control'], 'no-store')
        self.assertEquals(response['Akamai-Cache-Control'], 'no-store')
