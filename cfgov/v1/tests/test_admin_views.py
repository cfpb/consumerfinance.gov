from datetime import date
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from wagtail.core.models import Site
from wagtail.tests.testapp.models import SimplePage

from v1.admin_views import ExportFeedbackView
from v1.tests.wagtail_pages.helpers import save_new_page


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


cache_path = "wagtail.contrib.frontend_cache.backends.CloudfrontBackend"


@override_settings(
    WAGTAILFRONTENDCACHE={
        "akamai": {
            "BACKEND": "v1.models.caching.AkamaiBackend",
            "CLIENT_TOKEN": "fake",
            "CLIENT_SECRET": "fake",
            "ACCESS_TOKEN": "fake",
        },
        "files": {
            "BACKEND": cache_path,
            "DISTRIBUTION_ID": {"files.fake.gov": "fake"},
        },
    }
)
class TestCDNManagementView(TestCase):
    def setUp(self):
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

    @mock.patch("v1.models.caching.AkamaiBackend.purge")
    def test_submission_with_url_akamai(self, mock_purge):
        self.client.login(username="cdn", password="password")
        self.client.post(reverse("manage-cdn"), {"url": "http://www.fake.gov"})
        mock_purge.assert_called_with("http://www.fake.gov")

    @mock.patch(f"{cache_path}.purge_batch")
    def test_submission_with_url_cloudfront(self, mock_purge_batch):
        self.client.login(username="cdn", password="password")
        self.client.post(
            reverse("manage-cdn"), {"url": "http://files.fake.gov"}
        )
        mock_purge_batch.assert_called_with(["http://files.fake.gov"])

    @mock.patch("v1.models.caching.AkamaiBackend.purge_all")
    def test_submission_without_url(self, mock_purge_all):
        self.client.login(username="cdn", password="password")
        self.client.post(reverse("manage-cdn"))
        mock_purge_all.assert_any_call()

    def test_bad_submission(self):
        self.client.login(username="cdn", password="password")
        response = self.client.post(
            reverse("manage-cdn"), {"url": "not a URL"}
        )
        self.assertContains(response, "url: Enter a valid URL.")


class TestCDNManagerNotEnabled(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="superuser", email="", password="password"
        )

    def test_cdnmanager_not_enabled(self):
        self.client.login(username="superuser", password="password")
        response = self.client.get(reverse("manage-cdn"))
        expected_message = "CDN management is not currently enabled"
        self.assertContains(response, expected_message)


class TestExportFeedbackView(TestCase):
    def test_get_most_recent_quarter_jan1(self):
        self.assertEqual(
            ExportFeedbackView.get_most_recent_quarter(date(2019, 1, 1)),
            (date(2018, 10, 1), date(2018, 12, 31)),
        )

    def test_get_most_recent_quarter_mar31(self):
        self.assertEqual(
            ExportFeedbackView.get_most_recent_quarter(date(2019, 3, 31)),
            (date(2018, 10, 1), date(2018, 12, 31)),
        )

    def test_get_most_recent_quarter_apr1(self):
        self.assertEqual(
            ExportFeedbackView.get_most_recent_quarter(date(2019, 4, 1)),
            (date(2019, 1, 1), date(2019, 3, 31)),
        )

    def test_post_generates_zipfile(self):
        root_page = Site.objects.get(is_default_site=True).root_page
        save_new_page(
            SimplePage(title="Ask CFPB", slug="ask-cfpb", content="ask cfpb"),
            root=root_page,
        )
        save_new_page(
            SimplePage(
                title="Obtener respuestas",
                slug="obtener-respuestas",
                content="obtener respuestas",
            ),
            root=root_page,
        )
        save_new_page(
            SimplePage(
                title="Buying a House",
                slug="owning-a-home",
                content="buying a house",
            ),
            root=root_page,
        )

        request = RequestFactory().post(
            "/", {"from_date": "2019-01-01", "to_date": "2019-03-31"}
        )
        request.user = get_user_model().objects.get(is_superuser=True)

        response = ExportFeedbackView.as_view()(request)

        self.assertEqual(response["Content-Type"], "application/zip")
        self.assertEqual(
            response["Content-Disposition"],
            "attachment;filename=feedback_20190101_to_20190331.zip",
        )
