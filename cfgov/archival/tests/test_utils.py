import json
import logging

from django.test import TestCase

from wagtail.models import Site

from archival.utils import (
    export_page,
    get_last_migration,
    import_page,
)
from v1.models import BlogPage


class LastMigrationTestCase(TestCase):
    def test_get_last_migration_has_migrations(self):
        app_label = BlogPage._meta.app_label
        last_migration = get_last_migration(app_label)
        self.assertNotEqual(last_migration, "")

    def test_get_last_migration_no_migrations(self):
        last_migration = get_last_migration("nonexistent")
        self.assertEqual(last_migration, "")


class ExportPageTestCase(TestCase):
    def setUp(self):
        self.page = BlogPage(
            title="Test page",
            slug="test-page",
            content=json.dumps(
                [
                    {
                        "type": "full_width_text",
                        "value": [
                            {
                                "type": "content",
                                "content": "Hello, world!",
                            }
                        ],
                    }
                ]
            ),
            live=True,
        )

    def test_export_page(self):
        page_json = export_page(self.page)
        page_data = json.loads(page_json)

        self.assertEqual(page_data["app_label"], "v1")
        self.assertEqual(page_data["model"], "blogpage")
        self.assertEqual(page_data["data"]["title"], self.page.title)
        self.assertEqual(page_data["data"]["slug"], self.page.slug)

        self.assertListEqual(
            page_data["data"]["content"],
            list(self.page.content.raw_data),
        )


class ImportPageTestCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.original_page = BlogPage(
            title="Test page",
            slug="test-page",
            content=[("text", "Hello, world!")],
            live=True,
        )
        self.page_json = export_page(self.original_page)
        logging.disable(logging.NOTSET)

    def tearDown(self):
        logging.disable(logging.CRITICAL)

    def test_import_page_model_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "v1",
                "model": "PageModelDoesNotExist",
                "last_migration": "",
                "data": {},
            }
        )
        with self.assertRaises(LookupError):
            import_page(self.root_page, page_json)

    def test_import_page_app_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "app_does_not_exist",
                "model": "blogpage",
                "last_migration": "",
                "data": {},
            }
        )
        with self.assertRaises(LookupError):
            import_page(self.root_page, page_json)

    def test_import_page(self):
        page = import_page(self.root_page, self.page_json)

        self.assertEqual(page.title, self.original_page.title)
        self.assertEqual(page.slug, self.original_page.slug)
        self.assertEqual(page.content, self.original_page.content)
