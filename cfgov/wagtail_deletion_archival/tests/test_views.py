import json
from io import StringIO

from django.test import TestCase
from django.urls import reverse

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils

from v1.models import BlogPage
from wagtail_deletion_archival.utils import export_page


class ExportViewTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.page = BlogPage(
            title="Test page",
            slug="test-page",
            content=[("text", "Hello, world!")],
            live=True,
        )
        self.root_page.add_child(instance=self.page)
        self.page.save()

    def test_export_view(self):
        self.login()
        response = self.client.get(
            reverse("export_page", kwargs={"page_id": self.page.id})
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn("Content-Disposition", response.headers)
        self.assertEqual(
            response.headers["Content-Disposition"],
            'attachment; filename="test-page.json"',
        )

        self.assertIn("Content-Type", response.headers)
        self.assertEqual(response.headers["Content-Type"], "application/json")


class ImportViewTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

    def test_import_view_post_file(self):
        # Export a test page
        test_page = BlogPage(
            title="Test page",
            slug="test-page",
            content=[("text", "Hello, world!")],
            live=True,
        )
        page_json = export_page(test_page)
        page_io = StringIO(page_json)

        # Log in and post it
        self.login()
        response = self.client.post(
            reverse("import_page", kwargs={"page_id": self.root_page.id}),
            {"page_file": page_io},
        )
        self.assertEqual(response.status_code, 302)
        self.root_page.refresh_from_db()

        self.assertEqual(len(self.root_page.get_children()), 1)
        new_page = self.root_page.get_children().first()

        self.assertRedirects(
            response,
            reverse(
                "wagtailadmin_pages:edit", kwargs={"page_id": new_page.id}
            ),
            status_code=302,
        )

    def test_import_view_post_invalid(self):
        self.login()
        response = self.client.post(
            reverse("import_page", kwargs={"page_id": self.root_page.id}),
            {},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("page_file", response.context["form"].errors)

    def test_import_view_get(self):
        self.login()
        response = self.client.get(
            reverse("import_page", kwargs={"page_id": self.root_page.id}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_import_view_post_app_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "app_does_not_exist",
                "model": "blogpage",
                "last_migration": "",
                "data": {},
            }
        )
        page_io = StringIO(page_json)

        # Log in and post it
        self.login()
        response = self.client.post(
            reverse("import_page", kwargs={"page_id": self.root_page.id}),
            {"page_file": page_io},
        )
        self.assertTrue(len(response.context["form"].errors["page_file"]) > 0)
        self.assertIn(
            "There was an error importing this file as a page.",
            response.context["form"].errors["page_file"][0],
        )

    def test_import_view_post_model_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "v1",
                "model": "PageModelDoesNotExist",
                "last_migration": "",
                "data": {},
            }
        )
        page_io = StringIO(page_json)

        # Log in and post it
        self.login()
        response = self.client.post(
            reverse("import_page", kwargs={"page_id": self.root_page.id}),
            {"page_file": page_io},
        )
        self.assertTrue(len(response.context["form"].errors["page_file"]) > 0)
        self.assertIn(
            "There was an error importing this file as a page.",
            response.context["form"].errors["page_file"][0],
        )
