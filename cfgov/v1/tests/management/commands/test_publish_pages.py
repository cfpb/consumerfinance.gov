import tempfile
from contextlib import contextmanager

from django.core.management import call_command
from django.http import Http404
from django.test import TestCase

from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Site

from v1.models import BrowsePage


class PublishPagesTests(TestCase):
    def setUp(self):
        self.site_root = Site.objects.get(is_default_site=True).root_page
        self.pages = list(
            map(self.make_page_with_draft_revision, ["a", "b", "c"])
        )

    def make_page_with_draft_revision(self, slug):
        page = BrowsePage(title=slug, slug=slug, live=True)
        self.site_root.add_child(instance=page)

        page.title = f"{slug}-modified"
        page.live = False
        page.save_revision()

        return page

    @contextmanager
    def make_tempfile(self, content):
        with tempfile.NamedTemporaryFile() as tf:
            tf.write(content)
            tf.seek(0)
            yield tf

    def test_dry_run(self):
        with self.make_tempfile(b"/a/\n/b/\n/c/\n") as tf:
            call_command("publish_pages", "--dry-run", tf.name)

        for page in self.pages:
            page.refresh_from_db()
            self.assertEqual(page.revisions.count(), 1)
            self.assertNotIn("-modified", page.title)

    def test_ignore_missing(self):
        with self.make_tempfile(b"/a/\n/b/\n/c/\n/invalid/") as tf:
            with self.assertRaises(Http404):
                call_command("publish_pages", "--dry-run", tf.name)

            call_command(
                "publish_pages", "--dry-run", "--ignore-missing", tf.name
            )

    def test_publish(self):
        with self.make_tempfile(b"/a/\n/b/\n/c/\n") as tf:
            call_command("publish_pages", tf.name)

        for page in self.pages:
            page.refresh_from_db()
            self.assertEqual(page.revisions.count(), 2)
            self.assertIn("-modified", page.title)

    def test_handles_redirect(self):
        redirect_target = self.make_page_with_draft_revision("d")

        Redirect.objects.create(old_path="/e", redirect_page=redirect_target)

        redirect_target.refresh_from_db()
        self.assertEqual(redirect_target.revisions.count(), 1)
        self.assertNotIn("-modified", redirect_target.title)

        with self.make_tempfile(b"/e/\n") as tf:
            call_command("publish_pages", tf.name)

        redirect_target.refresh_from_db()
        self.assertEqual(redirect_target.revisions.count(), 2)
        self.assertIn("-modified", redirect_target.title)
