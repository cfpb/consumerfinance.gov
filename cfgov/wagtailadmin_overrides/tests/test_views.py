from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.test.utils import isolate_apps
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Site
from wagtail.tests.testapp.models import BusinessIndex, BusinessSubIndex
from wagtail.tests.utils import WagtailTestUtils

from v1.models import BrowsePage


class TestAddSubpage(TestCase, WagtailTestUtils):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page
        self.user = self.login()

    def test_overridden_view(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add_subpage", args=(self.root_page.id,)
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a page")

    def test_view_forbidden_if_user_lacks_permission(self):
        # This test duplicates the logic from
        # wagtail.admin.tests.pages.test_create_page.TestPageCreation.test_add_subpage_bad_permissions.
        self.user.is_superuser = False
        self.user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="wagtailadmin", codename="access_admin"
            )
        )
        self.user.save()

        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add_subpage", args=(self.root_page.id,)
            )
        )

        self.assertRedirects(response, reverse("wagtailadmin_home"))

    @isolate_apps()
    def test_descriptions_hidden_from_inherited_page_types(self):
        class InheritingPageWithoutDescription(BrowsePage):
            class Meta:
                pass

        with patch(
            "v1.models.BrowsePage.page_description", "I am a BrowsePage"
        ):
            response = self.client.get(
                reverse(
                    "wagtailadmin_pages:add_subpage", args=(self.root_page.id,)
                )
            )

            self.assertEqual(response.status_code, 200)

            # If we didn't hide descriptions on inherited page types without
            # their own page_description, the response would include this
            # description more than once.
            self.assertContains(response, "I am a BrowsePage", count=1)

    def test_lazy_description(self):
        page = BrowsePage(title="test", slug="test")
        self.root_page.add_child(instance=page)

        # Use a string that we know has already been translated.
        with patch(
            "v1.models.BrowsePage.page_description", _("Submit a Complaint")
        ):
            response = self.client.get(
                reverse("wagtailadmin_pages:add_subpage", args=(page.id,))
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Submit a Complaint")

    def test_invalid_description_ignored(self):
        with patch("v1.models.BrowsePage.page_description", 24601):
            response = self.client.get(
                reverse(
                    "wagtailadmin_pages:add_subpage", args=(self.root_page.id,)
                )
            )

            self.assertEqual(response.status_code, 200)

    def test_redirects_if_only_single_page_type_available(self):
        # We don't currently have a good example of this in our codebase, so
        # in order to test this we can use some Wagtail page types. This test
        # duplicates the logic from
        # wagtail.admin.tests.pages.test_create_page.TestPageCreation.test_add_subpage_with_one_valid_subpage_type.
        parent = BusinessIndex(title="parent", slug="parent")
        self.root_page.add_child(instance=parent)
        child = BusinessSubIndex(title="child", slug="child")
        parent.add_child(instance=child)

        response = self.client.get(
            reverse("wagtailadmin_pages:add_subpage", args=(child.id,))
        )

        self.assertRedirects(
            response,
            reverse(
                "wagtailadmin_pages:add",
                args=("tests", "businesschild", child.id),
            ),
        )
