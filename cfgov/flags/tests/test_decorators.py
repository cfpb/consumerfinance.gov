from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase
from mock import Mock

from flags.decorators import flag_required
from flags.models import Flag


class FlagRequiredTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAG_REQUIRED_TEST_CASE'

        self.request = HttpRequest()
        self.request.META['SERVER_NAME'] = 'localhost'
        self.request.META['SERVER_PORT'] = 8000

        self.view = Mock(__name__='view')

    def test_decorated_no_flag_exists(self):
        decorated = flag_required(self.flag_name)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_decorated_flag_disabled(self):
        decorated = flag_required(self.flag_name)(self.view)
        self.assertRaises(Http404, decorated, self.request)
        self.assertEqual(self.view.call_count, 0)

    def test_decorated_flag_enabled(self):
        def view(request):
            return HttpResponse('ok')

        Flag.objects.create(key=self.flag_name, enabled_by_default=True)
        decorated = flag_required(self.flag_name)(view)
        response = decorated(self.request)
        self.assertEqual(response.content, 'ok')

    def test_fallback_view(self):
        def fallback(request):
            return HttpResponse('fallback')

        decorator = flag_required(self.flag_name, fallback_view=fallback)
        decorated = decorator(self.view)
        response = decorated(self.request)
        self.assertEqual(response.content, 'fallback')
