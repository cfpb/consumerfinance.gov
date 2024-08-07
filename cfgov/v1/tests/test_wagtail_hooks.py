from django.contrib.auth.models import Permission
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils
from wagtail.whitelist import Whitelister as Allowlister

from v1.models import BlogPage, InternalDocsSettings


class TestAllowlistOverride(SimpleTestCase):
    # Borrowed from https://github.com/wagtail/wagtail/blob/master/wagtail
    # /core/tests/test_whitelist.py

    def setUp(self):
        self.allowlister = Allowlister()

    def test_allowlist_hooks(self):
        """
        Allowlister.clean should remove disallowed tags and attributes from
        a string
        """
        input_html = '<scan class="id">Consumer <embed>Finance</embed></scan>'
        output_html = self.allowlister.clean(input_html)
        self.assertHTMLEqual(output_html, "Consumer Finance")


class TestDjangoAdminLink(TestCase, WagtailTestUtils):
    def get_admin_response_for_user(self, is_staff):
        credentials = {"username": "regular", "password": "regular"}
        user = self.create_user(is_staff=is_staff, **credentials)

        user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="wagtailadmin", codename="access_admin"
            )
        )
        user.save()

        self.login(**credentials)
        return self.client.get(reverse("wagtailadmin_home"))

    def test_staff_sees_django_admin_link(self):
        response = self.get_admin_response_for_user(is_staff=True)
        self.assertContains(response, "Django Admin")

    def test_non_staff_doesnt_see_django_admin_link(self):
        response = self.get_admin_response_for_user(is_staff=False)
        self.assertNotContains(response, "Django Admin")


class TestInternalDocsLink(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def get_admin_response(self):
        return self.client.get(reverse("wagtailadmin_home"))

    def test_docs_not_defined_no_link_in_admin(self):
        self.assertNotContains(
            self.get_admin_response(), "/admin/internal-docs/"
        )

    def test_guide_defined_creates_link_in_admin(self):
        InternalDocsSettings.objects.create(url="https://example.com/")
        self.assertContains(self.get_admin_response(), "/admin/internal-docs/")


class LockedPageDeletionTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        root_page = Site.objects.get(is_default_site=True).root_page

        self.locked_page = BlogPage(title="locked page", slug="locked-page")
        self.locked_page.locked = True
        root_page.add_child(instance=self.locked_page)

        self.unlocked_page = BlogPage(
            title="unlocked page", slug="unlocked-page"
        )
        root_page.add_child(instance=self.unlocked_page)

    def test_delete_locked_page(self):
        response = self.client.post(
            reverse("wagtailadmin_pages:delete", args=(self.locked_page.pk,))
        )
        self.assertTrue(any("message" in ctx for ctx in response.context))
        self.assertEqual(
            "locked page is locked and cannot be deleted.",
            next(
                ctx["message"] for ctx in response.context if "message" in ctx
            ),
        )
        self.assertRedirects(
            response,
            reverse("wagtailadmin_explore", args=(self.locked_page.pk,)),
        )
        self.assertEqual(
            self.locked_page, BlogPage.objects.get(pk=self.locked_page.pk)
        )

    def test_bulk_delete_locked_page(self):
        response = self.client.post(
            reverse(
                "wagtail_bulk_action",
                args=(
                    "wagtailcore",
                    "page",
                    "delete",
                ),
            )
            + f"?id={self.locked_page.pk}&id={self.unlocked_page.pk}"
        )
        self.assertTrue(any("message" in ctx for ctx in response.context))
        self.assertIn(
            "locked page is locked and cannot be deleted.",
            next(
                ctx["message"] for ctx in response.context if "message" in ctx
            ),
        )
        self.assertRedirects(response, reverse("wagtailadmin_home"))

    def test_bulk_delete_locked_page_with_referrer(self):
        response = self.client.post(
            reverse(
                "wagtail_bulk_action",
                args=(
                    "wagtailcore",
                    "page",
                    "delete",
                ),
            )
            + f"?id={self.locked_page.pk}&id={self.unlocked_page.pk}",
            HTTP_REFERER="/",
        )
        self.assertTrue(any("message" in ctx for ctx in response.context))
        self.assertIn(
            "locked page is locked and cannot be deleted.",
            next(
                ctx["message"] for ctx in response.context if "message" in ctx
            ),
        )
        self.assertRedirects(response, "/")
