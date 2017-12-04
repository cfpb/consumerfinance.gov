import itertools

from unittest import TestCase

from v1.util.ref import categories, get_appropriate_categories


class TestCategories(TestCase):
    def test_no_duplicate_slugs(self):
        page_categories = dict(categories).values()
        slugs = list(itertools.chain(*(
            dict(page_category).keys() for page_category in page_categories
        )))
        self.assertItemsEqual(slugs, set(slugs))


class TestGetAppropriateCategories(TestCase):
# Note this test is heavily hard-coded with values from cfgov/v1/util/ref.py
    def test_non_related_post_category_should_not_return_matches(self):
        result = get_appropriate_categories(['Administrative adjudication'], 'blog')
        self.assertEqual(result, [])

    def test_related_post_category_should_not_return_matches_if_wrong_page_type(self):
        result = get_appropriate_categories(['Press Release'], 'blog')
        self.assertEqual(result, [])

    def test_should_return_matches_only_for_relevant_page_type(self):
        result = get_appropriate_categories(['Press Release', 'At the CFPB'], 'blog')
        self.assertEqual(len(result), 1)

    def test_should_return_matches_as_slugs(self):
        result = get_appropriate_categories(['Press Release'], 'newsroom')
        self.assertEqual(result, ['press-release'])

    def test_should_return_all_matches(self):
        result = get_appropriate_categories(['Op-Ed', 'Testimony', 'Speech', 'Press Release'], 'newsroom')
        self.assertEqual(len(result), 4)

