from unittest import TestCase

from paying_for_college.documents import SchoolDocument
from paying_for_college.models import School


class SchoolDocumentTest(TestCase):

    def test_prepare(self):
        school = School(school_id="999999",
                        settlement_school="Example University",
                        city="Example City", state="VA")
        doc = SchoolDocument()

        prepared_data = doc.prepare(school)
        self.assertEqual(prepared_data, {
            'autocomplete': doc.prepare_autocomplete(school),
            'city': school.city,
            'nicknames': doc.prepare_nicknames(school),
            'school_id': school.school_id,
            'state': school.state,
            'text': school.settlement_school,
        })
