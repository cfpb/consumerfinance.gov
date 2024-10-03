import json
from glob import glob
from unittest import skipIf

from django.conf import settings
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils

from freezegun import freeze_time

from v1.models import BlogPage
from wagtail_deletion_archival.tests.temp_storage import (
    uses_temp_archive_storage,
)
from wagtail_deletion_archival.utils import (
    convert_page_to_json,
    get_archive_storage,
    get_last_migration,
    import_page,
    make_archive_filename,
)


class GetArchivalStorageTests(SimpleTestCase):
    @override_settings(STORAGES={})
    def test_no_archival_storage(self):
        self.assertIsNone(get_archive_storage())

    @override_settings(
        STORAGES={
            "wagtail_deletion_archival": {
                "BACKEND": "django.core.files.storage.FileSystemStorage"
            }
        }
    )
    def test_archive_storage(self):
        self.assertIsNotNone(get_archive_storage())


@skipIf(settings.SKIP_DJANGO_MIGRATIONS, "Requires Django migrations")
class LastMigrationTestCase(TestCase):
    def test_get_last_migration_has_migrations(self):
        app_label = BlogPage._meta.app_label
        last_migration = get_last_migration(app_label)
        self.assertNotEqual(last_migration, "")

    def test_get_last_migration_no_migrations(self):
        last_migration = get_last_migration("nonexistent")
        self.assertEqual(last_migration, "")


@skipIf(settings.SKIP_DJANGO_MIGRATIONS, "Requires Django migrations")
class ConvertPageToJsonTestCase(TestCase):
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
        page_json = convert_page_to_json(self.page)
        page_data = json.loads(page_json)

        self.assertEqual(page_data["app_label"], "v1")
        self.assertEqual(page_data["model"], "blogpage")
        self.assertEqual(page_data["data"]["title"], self.page.title)
        self.assertEqual(page_data["data"]["slug"], self.page.slug)

        self.assertListEqual(
            page_data["data"]["content"],
            list(self.page.content.raw_data),
        )


@skipIf(settings.SKIP_DJANGO_MIGRATIONS, "Requires Django migrations")
class ImportPageTestCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.original_page = BlogPage(
            title="Test page",
            slug="test-page",
            content=[("text", "Hello, world!")],
            live=True,
        )
        self.page_json = convert_page_to_json(self.original_page)

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


class MakeArchiveFilenameTests(SimpleTestCase):
    @freeze_time("2020-01-01")
    def test_make_archive_filename(self):
        self.assertEqual(
            make_archive_filename("foo"), "foo-2020-01-01T00:00:00+00:00.json"
        )


@skipIf(settings.SKIP_DJANGO_MIGRATIONS, "Requires Django migrations")
class ArchivePageOnDeletionTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        root_page = Site.objects.get(is_default_site=True).root_page

        self.test_page1 = BlogPage(title="test page 1", slug="test-page1")
        root_page.add_child(instance=self.test_page1)

        self.test_child_page = BlogPage(title="child page", slug="test-child")
        self.test_page1.add_child(instance=self.test_child_page)

        self.test_page2 = BlogPage(title="test page 2", slug="test-page2")
        root_page.add_child(instance=self.test_page2)

        self.test_page3 = BlogPage(title="test page 3", slug="test-page3")
        root_page.add_child(instance=self.test_page3)

    @uses_temp_archive_storage()
    def test_delete_page(self, temp_storage):
        # Before the test no JSON files exist in the archive dir.
        self.assertFalse(glob(f"{temp_storage}/**/*.json", recursive=True))

        self.client.post(
            reverse("wagtailadmin_pages:delete", args=(self.test_page1.pk,))
        )

        # The page slug exists in the archive dir.
        self.assertTrue(
            glob(
                f"{temp_storage}/{self.test_page1.slug}/*.json",
                recursive=True,
            )
        )

        # The child page slug exists in the archive dir.
        self.assertTrue(
            glob(
                f"{temp_storage}/{self.test_page1.slug}/{self.test_child_page.slug}/*.json",
                recursive=True,
            )
        )

    @uses_temp_archive_storage()
    def test_bulk_delete_page(self, temp_storage):
        self.client.post(
            reverse(
                "wagtail_bulk_action",
                args=(
                    "wagtailcore",
                    "page",
                    "delete",
                ),
            )
            + f"?id={self.test_page1.pk}&id={self.test_page2.pk}"
        )

        # Page 1, its child page, and Page 2 should all be archived.
        self.assertEqual(
            len(
                glob(
                    f"{temp_storage}/**/*.json",
                    recursive=True,
                )
            ),
            3,
        )

    @uses_temp_archive_storage()
    def test_delete_page_confirmation(self, temp_storage):
        self.client.get(
            reverse("wagtailadmin_pages:delete", args=(self.test_page3.pk,))
        )
        self.assertFalse(glob(f"{temp_storage}/**/*.json", recursive=True))


class ArchivePageOnDeletionWhenArchivingIsDisabledTestCase(
    TestCase, WagtailTestUtils
):
    def test_delete_works_when_archiving_is_disabled(self):
        self.assertIsNone(get_archive_storage())

        root_page = Site.objects.get(is_default_site=True).root_page
        self.test_page1 = BlogPage(title="test page 1", slug="test-page1")
        root_page.add_child(instance=self.test_page1)

        self.login()
        self.client.post(
            reverse("wagtailadmin_pages:delete", args=(self.test_page1.pk,))
        )

        with self.assertRaises(BlogPage.DoesNotExist):
            BlogPage.objects.get(slug="test-page1")
