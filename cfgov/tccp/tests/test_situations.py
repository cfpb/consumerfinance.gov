from django.test import SimpleTestCase

from tccp.situations import SITUATIONS, get_situation_by_title


class SituationTests(SimpleTestCase):
    def test_get_situation_by_title_valid(self):
        self.assertEqual(
            get_situation_by_title("Have a lower monthly payment"),
            SITUATIONS[0],
        )

    def test_get_situation_by_title_invalid(self):
        with self.assertRaises(KeyError):
            get_situation_by_title("invalid")
