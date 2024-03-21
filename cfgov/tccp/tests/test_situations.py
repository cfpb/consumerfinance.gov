from itertools import product

from django.test import SimpleTestCase

from tccp.situations import SITUATIONS, Situation, get_situation_by_title


class SituationTests(SimpleTestCase):
    def test_get_situation_by_title_valid(self):
        self.assertEqual(
            get_situation_by_title("Pay less interest"),
            SITUATIONS[0],
        )

    def test_get_situation_by_title_invalid(self):
        with self.assertRaises(KeyError):
            get_situation_by_title("invalid")

    def test_get_nonconflicting_params(self):
        self.assertEqual(
            Situation.get_nonconflicting_params(
                [
                    Situation("one", {"a": 1, "b": 2}),
                    Situation("two", {"c": [3, 4]}),
                    Situation("three", {"a": 5, "b": 2}),
                ]
            ),
            {"b": 2, "c": [3, 4]},
        )

    def test_get_get_nonconflicting_params_multiple_duplicates(self):
        self.assertEqual(
            Situation.get_nonconflicting_params(
                [
                    Situation("one", {"a": 1}),
                    Situation("two", {"a": 2}),
                    Situation("three", {"a": 1}),
                ]
            ),
            {},
        )


class SituationContentTests(SimpleTestCase):
    def test_situation_content(self):
        for situation, content in product(SITUATIONS, ["select", "results"]):
            with self.subTest(title=situation.title, content=content):
                self.assertTrue(getattr(situation, f"{content}_html"))
