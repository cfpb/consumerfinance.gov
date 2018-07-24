from importlib import import_module

from django.apps import apps
from django.test import TestCase

from wagtail.wagtailcore.models import Page, Site


class TestMigration0116(TestCase):
    def setUp(self):
        self.migration = import_module(
            'v1.migrations.0116_single_wagtail_site'
        )

    def test_leaves_single_site_alone(self):
        self.assertEqual(Site.objects.count(), 1)
        self.migration.delete_non_default_wagtail_sites(apps, None)
        self.assertEqual(Site.objects.count(), 1)

    def test_deletes_non_default_site(self):
        Site.objects.create(
            hostname='foo.com',
            root_page=Page.objects.first(),
            is_default_site=False
        )
        Site.objects.get(is_default_site=True)
        self.migration.delete_non_default_wagtail_sites(apps, None)
        with self.assertRaises(Site.DoesNotExist):
            Site.objects.get(is_default_site=False)
