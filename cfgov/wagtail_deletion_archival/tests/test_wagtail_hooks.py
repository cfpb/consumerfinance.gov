from django.shortcuts import reverse
from django.test import TestCase

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils


class TestPageImportButton(WagtailTestUtils, TestCase):
    def test_page_import_button_renders(self):
        self.login()

        root_page = Site.objects.get(is_default_site=True).root_page
        response = self.client.get(
            reverse("wagtailadmin_explore", args=(root_page.pk,))
        )

        import_url = reverse(
            "wagtail_deletion_archive_import", args=(root_page.pk,)
        )
        self.assertContains(response, f'<a href="{import_url}"')
