from collections import Counter
from operator import itemgetter
from unittest import TestCase

from v1.util.ref import (
    categories,
    get_appropriate_categories,
    get_category_children,
)


class TestGetAppropriateCategories(TestCase):
    # This test is heavily hard-coded with values from cfgov/v1/util/ref.py.
    def test_non_related_post_category_no_matches(self):
        result = get_appropriate_categories(
            ["Administrative adjudication"], "blog"
        )
        self.assertEqual(result, [])

    def test_related_post_category_no_matches_if_wrong_page_type(self):
        result = get_appropriate_categories(["Press Release"], "blog")
        self.assertEqual(result, [])

    def test_should_return_matches_only_for_relevant_page_type(self):
        result = get_appropriate_categories(
            ["Press Release", "At the CFPB"], "blog"
        )
        self.assertEqual(len(result), 1)

    def test_should_return_matches_as_slugs(self):
        result = get_appropriate_categories(["Press Release"], "newsroom")
        self.assertEqual(result, ["press-release"])

    def test_should_return_all_matches(self):
        result = get_appropriate_categories(
            ["Op-Ed", "Testimony", "Speech", "Press Release"], "newsroom"
        )
        self.assertEqual(len(result), 4)


class TestGetCategoryChildren(TestCase):
    def test_get_children_of_single_category(self):
        self.assertEqual(
            get_category_children(["Amicus Brief"]),
            [
                "fed-circuit-court",
                "fed-district-court",
                "state-court",
                "us-supreme-court",
            ],
        )

    def test_get_children_of_multiple_categories(self):
        self.assertEqual(
            get_category_children(["Final rule", "Rule Under Development"]),
            [
                "final-rule",
                "interim-final-rule",
                "notice-proposed-rule-2",
                "proposed-rule-2",
            ],
        )

    def test_get_children_with_invalid_category_raises_keyerror(self):
        with self.assertRaises(KeyError):
            get_category_children(["This is not a valid category"])


class CategoryTests(TestCase):
    def test_that_all_category_slugs_are_unique(self):
        counter = Counter()

        for _, subcategories in categories:
            counter.update(map(itemgetter(0), subcategories))

        duplicates = [
            category for category, count in counter.items() if count > 1
        ]

        if duplicates:
            self.fail(f"Duplicate categories: {', '.join(duplicates)}")
