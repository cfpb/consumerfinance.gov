from django.apps import apps
from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils

from v1.models import BlogPage
from wagtail_deletion_archival.wagtail_hooks import archive_page_data_receiver


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

        self.fs = apps.get_app_config("wagtail_deletion_archival").filesystem

    def test_delete_page(self):
        self.client.post(
            reverse("wagtailadmin_pages:delete", args=(self.test_page1.pk,))
        )

        # The page slug exists in the archive dir and has a JSON file in it
        self.assertIn(self.test_page1.slug, self.fs.listdir("/"))
        self.assertTrue(
            self.fs.glob(f"{self.test_page1.slug}/*.json").count().files > 0
        )

        # The child page slug exists in the archive dir and has a JSON file
        self.assertIn(
            self.test_child_page.slug,
            self.fs.listdir(f"{self.test_page1.slug}"),
        )
        self.assertTrue(
            self.fs.glob(
                f"{self.test_page1.slug}/"
                f"{self.test_child_page.slug}/*.json"
            )
            .count()
            .files
            > 0
        )

    def test_bulk_delete_page(self):
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

        # The page slug exists in the archive dir
        self.assertIn(self.test_page2.slug, self.fs.listdir("/"))

        # And has a JSON file in it
        self.assertTrue(
            self.fs.glob(f"{self.test_page2.slug}/*.json").count().files > 0
        )

    def test_delete_page_confirmation(self):
        self.client.get(
            reverse("wagtailadmin_pages:delete", args=(self.test_page3.pk,))
        )
        self.assertEqual(
            self.fs.glob(f"{self.test_page3.slug}/*.json").count().files,
            0,
        )

    @override_settings(WAGTAIL_DELETION_ARCHIVE_FILESYSTEM=None)
    def test_delete_page_with_no_archive_dir(self):
        archive_page_data_receiver(None, self.test_page3)

        # There should be no test-page3 directory anywhere in the filesystem
        self.assertEqual(
            self.fs.glob(f"**/{self.test_page3.slug}/").count().directories, 0
        )
