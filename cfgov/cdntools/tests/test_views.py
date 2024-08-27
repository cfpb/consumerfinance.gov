from unittest import mock

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from django.urls import reverse

from requests.exceptions import HTTPError

from cdntools.backends import MOCK_PURGED


def create_admin_access_permissions():
    """
    This is to ensure that Wagtail's non-model permissions are set-up
    (needed for some of the tests below)
    Adapted from function of the same name in
    https://github.com/wagtail/wagtail/blob/master/wagtail/wagtailadmin/migrations/0001_create_admin_access_permissions.py
    """
    # Add a fake content type to hang the 'can access Wagtail admin'
    # permission off.
    wagtailadmin_content_type, created = ContentType.objects.get_or_create(
        app_label="wagtailadmin", model="admin"
    )

    # Create admin permission
    admin_permission, created = Permission.objects.get_or_create(
        content_type=wagtailadmin_content_type,
        codename="access_admin",
        name="Can access Wagtail admin",
    )

    # Assign it to Editors and Moderators groups
    for group in Group.objects.filter(name__in=["Editors", "Moderators"]):
        group.permissions.add(admin_permission)


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "cdntools.backends.MockCacheBackend",
            "HOSTNAMES": [
                "www.fake.gov",
            ],
        },
        "files": {
            "BACKEND": "cdntools.backends.MockCacheBackend",
            "HOSTNAMES": [
                "files.fake.gov",
            ],
        },
    }
)
class TestCDNManagementView(TestCase):
    def setUp(self):
        # Reset cache purged URLs after each test
        MOCK_PURGED[:] = []

        create_admin_access_permissions()

        self.no_permission = User.objects.create_user(
            username="noperm", email="", password="password"
        )
        self.cdn_manager = User.objects.create_user(
            username="cdn", email="", password="password"
        )

        # Give CDN Manager permission to add history items
        cdn_permission = Permission.objects.get(name="Can add cdn history")
        self.cdn_manager.user_permissions.add(cdn_permission)

        # Add no_permission and cdn_manager to Editors group
        editors = Group.objects.get(name="Editors")
        self.no_permission.groups.add(editors)
        self.cdn_manager.groups.add(editors)

    def test_requires_authentication(self):
        response = self.client.get(reverse("manage-cdn"))
        expected_url = "/admin/login/?next=/admin/cdn/"
        self.assertRedirects(
            response, expected_url, fetch_redirect_response=False
        )

    def test_form_hiding(self):
        # users without 'Can add cdn history' can view the page,
        # but the form is hidden
        self.client.login(username="noperm", password="password")
        response = self.client.get(reverse("manage-cdn"))
        self.assertContains(response, "You do not have permission")

    def test_post_blocking(self):
        # similarly, users without 'Can add cdn history' are also
        # blocked from POST'ing
        self.client.login(username="noperm", password="password")
        response = self.client.post(reverse("manage-cdn"))
        self.assertEqual(response.status_code, 403)

    def test_user_with_permission(self):
        self.client.login(username="cdn", password="password")
        response = self.client.get(reverse("manage-cdn"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a full URL")

    def test_submission_with_url_akamai(self):
        self.client.login(username="cdn", password="password")
        self.client.post(
            reverse("manage-cdn"),
            {"url": "http://www.fake.gov/about-us"},
        )
        self.assertIn(
            "http://www.fake.gov/about-us",
            MOCK_PURGED,
        )

    def test_submission_with_url_cloudfront(self):
        self.client.login(username="cdn", password="password")
        self.client.post(
            reverse("manage-cdn"),
            {"url": "http://files.fake.gov/test.pdf"},
        )
        self.assertIn(
            "http://files.fake.gov/test.pdf",
            MOCK_PURGED,
        )

    def test_submission_without_url(self):
        self.client.login(username="cdn", password="password")
        self.client.post(reverse("manage-cdn"))
        self.assertIn(
            "__all__",
            MOCK_PURGED,
        )

    def test_bad_submission(self):
        self.client.login(username="cdn", password="password")
        response = self.client.post(
            reverse("manage-cdn"), {"url": "not a URL"}
        )
        self.assertContains(response, "url: Enter a valid URL.")

    @override_settings(WAGTAILFRONTENDCACHE=None)
    def test_cdnmanager_not_enabled(self):
        self.client.login(username="cdn", password="password")
        response = self.client.get(reverse("manage-cdn"))
        self.assertEqual(response.status_code, 404)

    @mock.patch("cdntools.views.purge")
    def test_purge_raises_exception(self, mock_purge):
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {
            "title": "HTTPERROR",
            "detail": "With details",
        }
        mock_purge.side_effect = [
            HTTPError(response=mock_response),
            Exception("A generic exception"),
        ]

        self.client.login(username="cdn", password="password")
        response = self.client.post(
            reverse("manage-cdn"), {"url": "http://fake.gov/test"}
        )
        self.assertContains(response, "HTTPERROR: With details")

        response = self.client.post(
            reverse("manage-cdn"), {"url": "http://fake.gov/test"}
        )
        self.assertContains(response, "A generic exception")
