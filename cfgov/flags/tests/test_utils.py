from django.test import TestCase
from wagtail.wagtailcore.models import Site

from flags.models import Flag, FlagState
from flags.utils import init_missing_flag_states_for_site


class InitMissingFlagStatesTestCase(TestCase):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.flag_names = ('FOO', 'BAR')
        for flag_name in self.flag_names:
            Flag.objects.create(key=flag_name)

    def get_test_flag_states(self):
        return FlagState.objects.filter(flag_id__in=self.flag_names)

    def test_none_existing(self):
        states = self.get_test_flag_states()
        self.assertFalse(states.exists())

        init_missing_flag_states_for_site(self.site)

        states = self.get_test_flag_states()
        self.assertEqual(states.count(), 2)
        self.assertFalse(FlagState.objects.get(flag_id='FOO').enabled)
        self.assertFalse(FlagState.objects.get(flag_id='BAR').enabled)

    def test_some_existing(self):
        FlagState.objects.create(flag_id='FOO', enabled=True, site=self.site)
        init_missing_flag_states_for_site(self.site)

        states = self.get_test_flag_states()
        self.assertEqual(states.count(), 2)
        self.assertTrue(FlagState.objects.get(flag_id='FOO').enabled)
        self.assertFalse(FlagState.objects.get(flag_id='BAR').enabled)
