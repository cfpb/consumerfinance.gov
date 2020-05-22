from django.core.management import call_command
from django.test import TestCase

import mock

from regulations3k.management.commands import update_regulation_index
from regulations3k.models import Section, SectionParagraph
from regulations3k.search_indexes import RegulationParagraphIndex


class RegulationIndexTestCase(TestCase):

    # a single reg branch: Part > EffectiveDate > Subpart > Section
    fixtures = ['tree_limb.json']
    index = RegulationParagraphIndex()

    def setUp(self):
        Section.objects.order_by('pk').first().extract_graphs()

    def test_extract_paragraphs(self):
        self.assertEqual(SectionParagraph.objects.count(), 13)

    def test_index(self):
        self.assertEqual(self.index.get_model(), SectionParagraph)
        self.assertEqual(self.index.index_queryset().count(), 13)
        self.assertIs(
            self.index.index_queryset().first().section.subpart.version.draft,
            False)

    @mock.patch('regulations3k.management.commands'
                '.update_regulation_index._run_haystack_update')
    def test_index_management_command(self, mock_haystack):
        SectionParagraph.objects.all().delete()
        self.assertEqual(SectionParagraph.objects.count(), 0)
        call_command('update_regulation_index')
        self.assertEqual(SectionParagraph.objects.count(), 113)
        self.assertEqual(mock_haystack.call_count, 1)

    @mock.patch('regulations3k.management.commands'
                '.update_regulation_index.call_command')
    def test_run_haystack_update(self, mock_call):
        update_regulation_index._run_haystack_update()
        self.assertEqual(mock_call.call_count, 1)
