import types

from django.http import HttpRequest
from django.test import TestCase
from mock import patch
from wagtail.wagtailcore.models import Site

from flags.models import Flag, FlagState
from flags.utils import conditional_include


class ConditionalIncludeTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)

        request = HttpRequest()
        request.META['SERVER_NAME'] = self.site.hostname
        request.META['SERVER_PORT'] = self.site.port

        patched_get_request = patch(
            'flags.template_functions.get_request',
            return_value=request
        )
        patched_get_request.start()
        self.addCleanup(patched_get_request.stop)

    def create_and_set_flag(self, key, enabled):
        flag = Flag.objects.create(key=key)
        FlagState.objects.create(flag=flag, site=self.site, enabled=enabled)

    def test_not_set_returns_empty_list(self):
        self.create_and_set_flag('cal', False)
        self.assertEqual(
            conditional_include('cal', 'cal.urls', namespace='cal'),
            []
        )

    def test_set_returns_urls(self):
        self.create_and_set_flag('cal', True)
        include = conditional_include('cal', 'cal.urls', namespace='cal')
        self.assertIsInstance(include[0], types.ModuleType)
        self.assertEqual(include[0].__name__, 'cal.urls')
        self.assertIsNone(include[1])
        self.assertEqual(include[2], 'cal')
