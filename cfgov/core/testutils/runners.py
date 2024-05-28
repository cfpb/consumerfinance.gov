import logging
import shutil
from contextlib import redirect_stdout
from io import StringIO

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from wagtail.coreutils import get_supported_content_language_variant
from wagtail.models import Collection, Locale, Page, Site

from django_slowtests.testrunner import DiscoverSlowestTestsRunner

from scripts import initial_data


class TestRunner(DiscoverSlowestTestsRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment()

        # The test settings use a custom MEDIA_ROOT for tests that write files
        # to disk. We want to clean up that location after the tests run.
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # Disable logging below CRITICAL during tests.
        logging.disable(logging.CRITICAL)

        return super().run_tests(test_labels, extra_tests, **kwargs)

    def setup_databases(self, **kwargs):
        dbs = super().setup_databases(**kwargs)

        # If dbs is empty, it means we don't have a test database; this can
        # happen if e.g. we're only running tests that don't require one.
        if dbs:
            # Some required Wagtail data (like the default site) are created in
            # data migrations. If we're skipping migrations when running
            # tests, we need to create this data ourselves.
            if settings.SKIP_DJANGO_MIGRATIONS:
                self.initial_wagtail_data()

            # Set up our own additional required test data.
            initial_data.run()

        return dbs

    def initial_wagtail_data(self):
        """Populate required Wagtail data.

        This logic comes from these Wagtail migrations:

        - wagtailcore.0001_squashed_0016_change_page_url_path_to_text_field
        - wagtailcore.0025_collection_initial_data
        - wagtailcore.0054_initial_locale
        - login.0005_add_default_user_group
        """
        # Create default Locale object.
        Locale.objects.create(
            language_code=get_supported_content_language_variant(
                settings.LANGUAGE_CODE
            ),
        )

        # Create Page content type.
        page_content_type, _ = ContentType.objects.get_or_create(
            model="page", app_label="wagtailcore"
        )

        # Create root Wagtail page.
        Page.objects.create(
            title="Root",
            slug="root",
            content_type=page_content_type,
            path="0001",
            depth=1,
            numchild=1,
            url_path="/",
        )

        # Create temporary homepage (this will be deleted by our initial_data).
        homepage = Page.objects.create(
            title="Welcome to your new Wagtail site!",
            slug="home",
            content_type=page_content_type,
            path="00010001",
            depth=2,
            numchild=0,
            url_path="/home/",
        )

        # Create default site (this will be updated by our initial_data).
        Site.objects.get_or_create(
            hostname="localhost",
            root_page_id=homepage.id,
            is_default_site=True,
        )

        # Create default collection.
        Collection.objects.create(
            name="Root",
            path="0001",
            depth=1,
            numchild=0,
        )

        # Create default groups.
        Group.objects.get_or_create(name="Editors")
        Group.objects.get_or_create(name="Moderators")
        Group.objects.get_or_create(name="Wagtail Users")


class StdoutCapturingTestRunner(TestRunner):
    def run_suite(self, suite, **kwargs):
        captured_stdout = StringIO()
        with redirect_stdout(captured_stdout):
            return_value = super().run_suite(suite, **kwargs)

        if captured_stdout.getvalue():
            raise RuntimeError(
                "unit tests should avoid writing to stdout: "
                f"{captured_stdout.getvalue()}"
            )

        return return_value
