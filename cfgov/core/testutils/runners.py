import importlib
import logging
import shutil
from contextlib import redirect_stdout
from io import StringIO

from django.apps import apps
from django.conf import settings
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.test.runner import DiscoverRunner

from scripts import initial_data


class TestRunner(DiscoverRunner):
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

        # Ensure that certain key data migrations are always run even if
        # tests are being run with most migrations disabled (e.g. using
        # settings.MIGRATION_MODULES).
        self.run_required_data_migrations()

        # Set up additional required test data that isn't contained in data
        # migrations, for example an admin user.
        initial_data.run()

        return dbs

    def run_required_data_migrations(self):
        if not settings.MIGRATION_MODULES:
            return

        migration_methods = (
            (
                "wagtailcore",
                "wagtail.core.migrations.0054_initial_locale",
                "initial_locale",
            ),
            (
                "wagtailcore",
                "wagtail.core.migrations.0002_initial_data",
                "initial_data",
            ),
            (
                "wagtailcore",
                "wagtail.core.migrations.0025_collection_initial_data",
                "initial_data",
            ),
        )

        loader = MigrationLoader(connection)

        for app_name, migration, method in migration_methods:
            if not self.is_migration_applied(loader, app_name, migration):
                print("applying migration {}".format(migration))
                module = importlib.import_module(migration)
                getattr(module, method)(apps, None)

    @staticmethod
    def is_migration_applied(loader, app_name, migration):
        migration_name = migration.split(".")[-1]
        return (app_name, migration_name) in loader.applied_migrations


class StdoutCapturingTestRunner(TestRunner):
    def run_suite(self, suite, **kwargs):
        captured_stdout = StringIO()
        with redirect_stdout(captured_stdout):
            return_value = super().run_suite(suite, **kwargs)

        if captured_stdout.getvalue():
            raise RuntimeError(
                "unit tests should avoid writing to stdout: {}".format(
                    captured_stdout.getvalue()
                )
            )

        return return_value
