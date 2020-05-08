from django.test import TestCase

from data_research.research_conference import get_conference_details_from_page


class GetConferenceDetailsFromPageTests(TestCase):
    fixtures = ['conference_registration_page']

    def test_gets_details_from_page(self):
        self.assertEqual(
            get_conference_details_from_page(99999),
            {
                'govdelivery_code': 'TEST-GOVDELIVERY-CODE',
                'capacity': 100,
            }
        )

    def test_no_block_on_page_raises_runtimeerror(self):
        with self.assertRaises(RuntimeError):
            get_conference_details_from_page(3)
