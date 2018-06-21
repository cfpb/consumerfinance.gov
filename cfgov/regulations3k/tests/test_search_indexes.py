from __future__ import unicode_literals

from django.test import TestCase

from regulations3k.models import Section
from regulations3k.search_indexes import RegulationSectionIndex


class RegulationIndexTestCase(TestCase):

    # a single reg branch: Part > EffectiveDate > Subpart > Section
    fixtures = ['tree_limb.json']
    index = RegulationSectionIndex()

    def test_index(self):
        self.assertEqual(self.index.get_model(), Section)
        self.assertEqual(self.index.index_queryset().count(), 4)
        self.assertIs(
            self.index.index_queryset().first().subpart.version.draft,
            False)
