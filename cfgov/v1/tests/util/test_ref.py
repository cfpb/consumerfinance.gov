import itertools

from unittest import TestCase

from v1.util.ref import categories


class TestCategories(TestCase):
    def test_no_duplicate_slugs(self):
        page_categories = dict(categories).values()
        slugs = list(itertools.chain(*(
            dict(page_category).keys() for page_category in page_categories
        )))
        self.assertItemsEqual(slugs, set(slugs))
