from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from regulations3k.management.commands import update_regulation_index
from regulations3k.models import Section, SectionParagraph


class RegulationIndexTestCase(TestCase):

    # a single reg branch: Part > EffectiveDate > Subpart > Section
    fixtures = ['tree_limb.json']

    def setUp(self):
        Section.objects.order_by('pk').first().extract_graphs()

    def test_extract_paragraphs(self):
        self.assertEqual(SectionParagraph.objects.count(), 13)

    @mock.patch('regulations3k.management.commands'
                '.update_regulation_index._run_elasticsearch_rebuild')
    def test_index_management_command(self, mock_elasticsearch):
        SectionParagraph.objects.all().delete()
        self.assertEqual(SectionParagraph.objects.count(), 0)
        call_command('update_regulation_index')
        self.assertEqual(SectionParagraph.objects.count(), 113)
        self.assertEqual(mock_elasticsearch.call_count, 1)

    @mock.patch('regulations3k.management.commands'
                '.update_regulation_index.call_command')
    def test_run_elasticsearch_rebuild(self, mock_call):
        update_regulation_index._run_elasticsearch_rebuild()
        self.assertEqual(mock_call.call_count, 1)
