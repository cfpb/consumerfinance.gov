from django.db import IntegrityError
from django.test import TestCase
from wagtail.wagtailcore.models import Site

from flags.models import Flag, FlagState


class FlagTestCase(TestCase):
    def test_default_disabled(self):
        flag = Flag.objects.create(key='FOO')
        self.assertFalse(flag.enabled_by_default)


class FlagStateTestCase(TestCase):
    def setUp(self):
        default_site = Site.objects.get(is_default_site=True)
        self.site1 = Site.objects.create(
            hostname='host1',
            root_page_id=default_site.root_page_id
        )
        self.site2 = Site.objects.create(
            hostname='host2',
            root_page_id=default_site.root_page_id
        )

    def test_multiple_sites(self):
        flag = Flag.objects.create(key='FOO')
        FlagState.objects.create(flag=flag, site=self.site1)

        try:
            FlagState.objects.create(flag=flag, site=self.site2)
        except IntegrityError:
            self.fail('different sites can have different flag states')

    def test_one_flag_state_per_site(self):
        flag = Flag.objects.create(key='FOO')
        FlagState.objects.create(flag=flag, site=self.site1)
        with self.assertRaises(IntegrityError):
            FlagState.objects.create(flag=flag, site=self.site1)
