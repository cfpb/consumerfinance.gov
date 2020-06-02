# -*- coding: utf8 -*-

from django.test import TestCase

from paying_for_college.models import School
from paying_for_college.search_indexes import SchoolIndex


class SchoolIndexTest(TestCase):
    fixtures = ['test_fixture.json']
    MOCK_INDEX = SchoolIndex()

    def test_index(self):
        self.assertTrue(self.MOCK_INDEX.get_model() == School)
        self.assertTrue(self.MOCK_INDEX.index_queryset().count() ==
                        School.objects.count())

        mock_obj = School.objects.get(pk=155317)
        self.assertIn(
            'Jayhawks',
            self.MOCK_INDEX.prepare_autocomplete(mock_obj)
        )
