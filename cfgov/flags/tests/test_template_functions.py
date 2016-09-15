from django.http import HttpRequest
from django.test import TestCase
from mock import Mock, patch
from wagtail.wagtailcore.models import Site

from flags.models import Flag, FlagState
from flags.template_functions import (
    flag_disabled, flag_enabled, flags_enabled
)


class FlagEnabledTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAG_ENABLED_TEST_CASE'
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_no_flag_should_be_disabled(self):
        self.assertFalse(flag_enabled(self.request, self.flag_name))

    def test_flag_default_false_disabled(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=False)
        self.assertFalse(flag_enabled(self.request, self.flag_name))

    def test_flag_default_true_enabled(self):
        Flag.objects.create(key=self.flag_name, enabled_by_default=True)
        self.assertTrue(flag_enabled(self.request, self.flag_name))

    def test_flag_false_disabled(self):
        flag = Flag.objects.create(key=self.flag_name)
        FlagState.objects.create(flag=flag, site=self.site, enabled=False)
        self.assertFalse(flag_enabled(self.request, self.flag_name))

    def test_flag_true_enabled(self):
        flag = Flag.objects.create(key=self.flag_name)
        FlagState.objects.create(flag=flag, site=self.site, enabled=True)
        self.assertTrue(flag_enabled(self.request, self.flag_name))

    def test_flag_for_other_site_disabled(self):
        flag = Flag.objects.create(key=self.flag_name)
        other_site = Site.objects.create(
            is_default_site=False,
            root_page_id=self.site.root_page_id
        )

        FlagState.objects.create(flag=flag, site=other_site, enabled=True)
        self.assertFalse(flag_enabled(self.request, self.flag_name))


class FlagDisabledTestCase(TestCase):
    def setUp(self):
        self.flag_name = 'FLAG_DISABLED_TEST_CASE'
        self.request = Mock()

    def test_flag_disabled_true(self):
        with patch(
            'flags.template_functions.flag_enabled',
            return_value=True
        ):
            self.assertFalse(flag_disabled(self.request, self.flag_name))

    def test_flag_disabled_false(self):
        with patch(
            'flags.template_functions.flag_enabled',
            return_value=False
        ):
            self.assertTrue(flag_disabled(self.request, self.flag_name))


class FlagsEnabledTestCase(TestCase):
    def setUp(self):
        self.flag_names = ('FOO', 'BAR', 'BAZ')
        self.request = Mock()

    def test_flags_enabled_all_true(self):
        with patch(
            'flags.template_functions.flag_enabled',
            side_effect=[True, True, True]
        ):
            self.assertTrue(flags_enabled(self.request, *self.flag_names))

    def test_flags_enabled_some_true(self):
        with patch(
            'flags.template_functions.flag_enabled',
            side_effect=[True, False, True]
        ):
            self.assertFalse(flags_enabled(self.request, *self.flag_names))
