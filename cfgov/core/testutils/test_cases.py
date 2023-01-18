from django.test import TestCase

from wagtail.models import Page, Site


class WagtailPageTreeTestCase(TestCase):
    """Mixin that creates a Wagtail page tree for tests.

    Test cases that inherit from this should define a get_page_tree()
    classmethod which returns a tree of pages as a nested list:

    [
        ParentPage,
        [
            ChildPage,
            ChildPage,
            [
                GrandchildPage,
                GrandchildPage,
            ],
        ],
    ]

    Pages returned from that method get added as children of the Wagtail
    default site root for the duration of the test case.

    The class variable `page_tree` can also be used by tests to reference
    pages that were added to the tree.
    """

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.get(is_default_site=True)

        cls.page_tree = cls._build_page_tree(
            site.root_page, cls.get_page_tree()
        )

    @classmethod
    def _build_page_tree(cls, root, page_tree):
        tree = []
        parent = root

        for node in page_tree:
            if isinstance(node, Page):
                root.add_child(instance=node)
                tree.append(node)
                parent = node
            else:
                tree.extend(cls._build_page_tree(parent, node))

        return tree

    @classmethod
    def get_page_tree(cls):
        raise NotImplementedError
