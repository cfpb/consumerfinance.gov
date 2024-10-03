import json
import os
import os.path
from io import StringIO
from unittest import skipIf

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils

from v1.models import BlogPage
from wagtail_deletion_archival.tests.temp_storage import (
    uses_temp_archive_storage,
)
from wagtail_deletion_archival.utils import (
    convert_page_to_json,
    get_archive_storage,
    make_archive_filename,
)


@skipIf(settings.SKIP_DJANGO_MIGRATIONS, "Requires Django migrations")
class ImportViewTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

    def test_import_view_get(self):
        self.login()
        response = self.client.get(
            reverse(
                "wagtail_deletion_archive_import",
                kwargs={"page_id": self.root_page.pk},
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def post_to_import_view(self, **kwargs):
        self.login()

        return self.client.post(
            reverse(
                "wagtail_deletion_archive_import",
                kwargs={"page_id": self.root_page.pk},
            ),
            kwargs,
        )

    def test_import_view_post_file(self):
        test_page = BlogPage(
            title="Test page",
            slug="test-page",
            content=[("text", "Hello, world!")],
            live=True,
        )
        page_json = convert_page_to_json(test_page)
        response = self.post_to_import_view(page_file=StringIO(page_json))

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
        response = self.post_to_import_view()

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("page_file", response.context["form"].errors)

    def test_import_view_post_app_does_not_exist(self):
        page_json = json.dumps(
            {
                "app_label": "app_does_not_exist",
                "model": "blogpage",
                "last_migration": "",
                "data": {},
            }
        )
        response = self.post_to_import_view(page_file=StringIO(page_json))

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
        response = self.post_to_import_view(page_file=StringIO(page_json))

        self.assertTrue(len(response.context["form"].errors["page_file"]) > 0)
        self.assertIn(
            "There was an error importing this file as a page.",
            response.context["form"].errors["page_file"][0],
        )


class ArchiveViewTests(WagtailTestUtils, TestCase):
    def test_no_storage_404(self):
        self.assertIsNone(get_archive_storage())

        self.login()
        response = self.client.get(reverse("wagtail_deletion_archive_index"))
        self.assertEqual(response.status_code, 404)

    @uses_temp_archive_storage()
    def test_valid_storage(self, temp_storage):
        os.mkdir(f"{temp_storage}/subdir")
        filename = make_archive_filename("test")
        open(os.path.join(temp_storage, "subdir", filename), "w").close()

        self.login()
        response = self.client.get(reverse("wagtail_deletion_archive_index"))
        self.assertContains(response, filename)

        response = self.client.get(
            reverse(
                "wagtail_deletion_archive_serve",
                kwargs={"path": f"subdir/{filename}"},
            )
        )
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="{filename}"',
        )

        response = self.client.get(
            reverse(
                "wagtail_deletion_archive_serve", kwargs={"path": "missing"}
            )
        )
        self.assertEqual(response.status_code, 404)
