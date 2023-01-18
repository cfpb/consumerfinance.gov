from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.test.utils import WagtailTestUtils


def overridden_home_view(request, *args, **kwargs):
    return HttpResponse("Overridden")


class WagtailAdminViewOverrideMiddlewareTests(TestCase, WagtailTestUtils):
    @override_settings()
    def test_noop_if_setting_is_not_defined(self):
        del settings.WAGTAILADMIN_OVERRIDDEN_VIEWS

        self.login()
        response = self.client.get(reverse("wagtailadmin_home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")
        self.assertNotContains(response, "Overridden")

    @override_settings(
        WAGTAILADMIN_OVERRIDDEN_VIEWS={
            "wagtailadmin_home": overridden_home_view,
        }
    )
    def test_overrides_view(self):
        self.login()
        response = self.client.get(reverse("wagtailadmin_home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Welcome")
        self.assertContains(response, "Overridden")

    @override_settings(
        WAGTAILADMIN_OVERRIDDEN_VIEWS={
            "wagtailadmin_home": overridden_home_view,
        }
    )
    def test_validates_that_user_has_proper_permissions(self):
        response = self.client.get(reverse("wagtailadmin_home"))

        self.assertEqual(response.status_code, 302)
        self.assertRegex(
            response["Location"], r"^" + reverse("wagtailadmin_login")
        )
