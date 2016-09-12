from django.test import TestCase
from wagtail.wagtailcore.models import Site

from flags.models import Flag, FlagState
from flags.utils import init_missing_flag_states_for_site


class InitMissingFlagStatesTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        Flag.objects.create(key='FOO')
        Flag.objects.create(key='BAR')

    def test_none_existing(self):
        self.assertFalse(FlagState.objects.exists())
        init_missing_flag_states_for_site(self.site)
        self.assertEqual(FlagState.objects.count(), 2)
        self.assertFalse(FlagState.objects.get(flag_id='FOO').enabled)
        self.assertFalse(FlagState.objects.get(flag_id='BAR').enabled)

    def test_some_existing(self):
        FlagState.objects.create(flag_id='FOO', enabled=True, site=self.site)
        init_missing_flag_states_for_site(self.site)
        self.assertEqual(FlagState.objects.count(), 2)
        self.assertTrue(FlagState.objects.get(flag_id='FOO').enabled)
        self.assertFalse(FlagState.objects.get(flag_id='BAR').enabled)
