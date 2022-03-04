from unittest import TestCase

from django.db import models

from paying_for_college.documents import SchoolDocument
from paying_for_college.models import School


class SchoolDocumentTest(TestCase):
    def test_get_queryset(self):
        qs = SchoolDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, School)

    def test_prepare(self):
        school = School(
            school_id="999999", city="Example City", state="VA", zip5="12345"
        )
        doc = SchoolDocument()

        prepared_data = doc.prepare(school)
        self.assertEqual(
            prepared_data,
            {
                "autocomplete": doc.prepare_autocomplete(school),
                "city": school.city,
                "nicknames": doc.prepare_nicknames(school),
                "school_id": school.school_id,
                "state": school.state,
                "text": school.primary_alias,
                "zip5": school.zip5,
                "url": doc.prepare_url(school),
            },
        )
