from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Site
from wagtail.tests.utils import WagtailTestUtils


class TestAddSubpage(TestCase, WagtailTestUtils):
    def test_overridden_add_subpage_view(self):
        root_page = Site.objects.get(is_default_site=True).root_page

        self.login()
        response = self.client.get(
            reverse("wagtailadmin_pages:add_subpage", args=(root_page.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a page")
