import importlib

from django.apps import apps
from django.test import TestCase
from django.utils.crypto import get_random_string

from v1.models import CFGOVPage, CFGOVPageCategory
from v1.tests.wagtail_pages.helpers import publish_page


class TestNewCategoriesMigration(TestCase):
    def setUp(self):
        self.migration = importlib.import_module(
            'v1.migrations.0054_new_categories'
        )

    def make_page_with_category(self, category):
        page = CFGOVPage(title='title', slug=get_random_string())
        publish_page(page)

        category = CFGOVPageCategory(page=page, name=category)
        category.save()

    def get_category_pages(self, category):
        return CFGOVPage.objects.filter(categories__name=category)

    def test_modify_categories(self):
        self.make_page_with_category('from')
        self.assertTrue(self.get_category_pages('from').exists())
        self.assertFalse(self.get_category_pages('to').exists())

        self.migration.change_categories(apps, 'from', 'to')
        self.assertFalse(self.get_category_pages('from').exists())
        self.assertTrue(self.get_category_pages('to').exists())

    def test_migrate_forwards(self):
        self.make_page_with_category('admin-filing')
        self.migration.migrate_forwards(apps, None)
        self.assertFalse(self.get_category_pages('admin-filing').exists())
        self.assertTrue(self.get_category_pages(
            'stipulation-and-consent-order-2'
        ).exists())

    def test_migrate_backwards(self):
        self.make_page_with_category('administrative-adjudication-2')
        self.make_page_with_category('stipulation-and-consent-order-2')
        self.assertFalse(
            self.get_category_pages('admin-filing').exists()
        )

        self.migration.migrate_backwards(apps, None)
        self.assertEqual(
            self.get_category_pages('admin-filing').count(),
            2
        )
