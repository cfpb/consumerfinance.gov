import argparse
import io
import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from wagtail.core.models import Site
from wagtail.tests.testapp.models import SimplePage


class SearchPageRevisionsTestCase(TestCase):

    def setUp(self):
        root_page = Site.objects.get(is_default_site=True).root_page
        self.page = SimplePage(title='Test', content='Testing', live=True)
        root_page.add_child(instance=self.page)
        self.revision = self.page.save_revision()
        call_command('wagtail_update_index', stdout=StringIO())

    def test_search_pagerevisions_stdout(self):
        stdout = StringIO()
        call_command('search_pagerevisions', 'test', stdout=stdout)
        outlines = str(stdout.getvalue()).splitlines()

        self.assertEqual(len(outlines), 2)
        self.assertIn(str(self.page.id), outlines[1])
        self.assertIn(str(self.revision.id), outlines[1])
        self.assertIn(
            f'/admin/pages/{self.page.id}/revisions/{self.revision.id}/view/',
            outlines[1]
        )

    def test_search_pagerevisions_to_file(self):
        with tempfile.NamedTemporaryFile() as tf:
            call_command('search_pagerevisions', 'test', filename=tf.name)

            with open(tf.name, encoding='utf-8') as f:
                outlines = f.readlines()
                self.assertEqual(len(outlines), 2)
                self.assertIn(str(self.page.id), outlines[1])
                self.assertIn(str(self.revision.id), outlines[1])
