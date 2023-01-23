import tempfile
from contextlib import contextmanager

from django.core.management import CommandError, call_command
from django.http import Http404
from django.test import TestCase

from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Site
from wagtail.tests.utils import WagtailTestUtils

from v1.models import BrowsePage


class TestImportTranslationLinks(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

        site_root = Site.objects.get(is_default_site=True).root_page

        self.english_page = BrowsePage(
            title="en", slug="en", language="en", live=True
        )
        site_root.add_child(instance=self.english_page)

        self.spanish_live_page = BrowsePage(
            title="es", slug="es", language="es", live=True
        )
        site_root.add_child(instance=self.spanish_live_page)
        self.spanish_live_page.save_revision().publish()

        self.spanish_live_and_draft_page = BrowsePage(
            title="es2", slug="es2", language="es", live=True
        )
        site_root.add_child(instance=self.spanish_live_and_draft_page)
        self.spanish_live_and_draft_page.save_revision()
        self.spanish_live_and_draft_page.title = "es2 changed"
        self.spanish_live_and_draft_page.save_revision()

    @contextmanager
    def make_tempfile(self, content):
        tf = tempfile.NamedTemporaryFile()
        tf.write(content)
        tf.seek(0)
        yield tf

    def test_dry_run(self):
        with self.make_tempfile(b"/es/,/en/\n/es2/,/en/\n") as tf:
            call_command("import_translation_links", "--dry-run", tf.name)

        self.assertEqual(self.spanish_live_page.revisions.count(), 1)
        self.assertIsNone(self.spanish_live_page.english_page)
        self.assertTrue(self.spanish_live_page.live)

        self.assertEqual(self.spanish_live_and_draft_page.revisions.count(), 2)
        self.assertIsNone(self.spanish_live_and_draft_page.english_page)
        self.assertTrue(self.spanish_live_and_draft_page.live)

    def test_invalid_path_fails(self):
        with self.make_tempfile(b"/invalid/,/en/\n") as tf:
            with self.assertRaises(Http404):
                call_command("import_translation_links", "--dry-run", tf.name)

    def test_save_requires_username(self):
        with self.make_tempfile(b"/es/,/en/\n/es2/,/en/\n") as tf:
            with self.assertRaises(CommandError):
                call_command("import_translation_links", tf.name)

    def test_save_draft_only(self):
        with self.make_tempfile(b"/es/,/en/\n/es2/,/en/\n") as tf:
            call_command(
                "import_translation_links",
                "--revision-username=test@email.com",
                tf.name,
            )

        self.spanish_live_page.refresh_from_db()
        self.spanish_live_and_draft_page.refresh_from_db()

        self.assertEqual(self.spanish_live_page.revisions.count(), 2)
        self.assertIsNone(self.spanish_live_page.english_page)
        self.assertTrue(self.spanish_live_page.live)
        self.assertEqual(
            self.spanish_live_page.get_latest_revision_as_page().english_page.pk,
            self.english_page.pk,
        )

        self.assertEqual(self.spanish_live_and_draft_page.revisions.count(), 3)
        self.assertIsNone(self.spanish_live_and_draft_page.english_page)
        self.assertTrue(self.spanish_live_and_draft_page.live)
        self.assertEqual(
            self.spanish_live_and_draft_page.get_latest_revision_as_page().english_page.pk,
            self.english_page.pk,
        )

    def test_handles_redirect(self):
        Redirect.objects.create(
            old_path="/redirected", redirect_page=self.spanish_live_page
        )

        with self.make_tempfile(b"/redirected/,/en/\n") as tf:
            call_command(
                "import_translation_links",
                "--revision-username=test@email.com",
                tf.name,
            )

        self.assertEqual(
            self.spanish_live_page.get_latest_revision_as_page().english_page.pk,
            self.english_page.pk,
        )

    def test_republish(self):
        with self.make_tempfile(b"/es/,/en/\n/es2/,/en/\n") as tf:
            call_command(
                "import_translation_links",
                "--revision-username=test@email.com",
                "--republish",
                tf.name,
            )

        self.spanish_live_page.refresh_from_db()
        self.spanish_live_and_draft_page.refresh_from_db()

        self.assertEqual(self.spanish_live_page.revisions.count(), 2)
        self.assertEqual(
            self.spanish_live_page.english_page.pk, self.english_page.pk
        )
        self.assertTrue(self.spanish_live_page.live)

        self.assertEqual(self.spanish_live_and_draft_page.revisions.count(), 3)
        self.assertIsNone(self.spanish_live_and_draft_page.english_page)
        self.assertTrue(self.spanish_live_and_draft_page.live)
        self.assertEqual(
            self.spanish_live_and_draft_page.get_latest_revision_as_page().english_page.pk,
            self.english_page.pk,
        )
