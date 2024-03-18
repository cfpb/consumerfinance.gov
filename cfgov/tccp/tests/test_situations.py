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

    def test_get_unique_params(self):
        self.assertEqual(
            Situation.get_unique_params(
                [{"a": 1, "b": 2}, {"c": [3, 4]}, {"a": 5, "b": 2}]
            ),
            {"b": 2, "c": [3, 4]},
        )

    def test_get_unique_params_multiple_duplicates(self):
        self.assertEqual(
            Situation.get_unique_params([{"a": 1}, {"a": 2}, {"a": 1}]),
            {},
        )

    def test_get_querystring(self):
        self.assertEqual(
            Situation.get_querystring({"a": 1, "b": [2, 3]}), "a=1&b=2&b=3"
        )

    def test_get_combined_query(self):
        self.assertEqual(
            Situation.get_combined_query(
                [Situation("foo", {"a": 1}), Situation("bar", {"b": 2})]
            ),
            "a=1&b=2",
        )


class SituationContentTests(SimpleTestCase):
    def test_situation_content(self):
        for situation, content in product(SITUATIONS, ["select", "results"]):
            with self.subTest(title=situation.title, content=content):
                self.assertTrue(getattr(situation, f"{content}_html"))
