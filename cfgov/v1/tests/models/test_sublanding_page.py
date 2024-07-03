import datetime as dt
import json

from django.test import RequestFactory, SimpleTestCase

from core.testutils.test_cases import WagtailPageTreeTestCase
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.models import AbstractFilterPage, BrowseFilterablePage, SublandingPage


class SublandingPageTestCase(ElasticsearchTestsMixin, WagtailPageTreeTestCase):
    """
    This test case checks that the browse-filterable posts of a sublanding
    page are properly retrieved.
    """

    @classmethod
    def get_page_tree(cls):
        return [
            (
                SublandingPage(
                    title="sublanding",
                    content=json.dumps(
                        [{"type": "post_preview_snapshot", "value": {}}]
                    ),
                ),
                [
                    (
                        BrowseFilterablePage(title="browse filterable 1"),
                        [
                            AbstractFilterPage(
                                title="child 1 of browse filterable 1",
                                date_published=dt.date(2016, 9, 1),
                            ),
                            AbstractFilterPage(
                                title="child 2 of browse filterable 1",
                                date_published=dt.date(2016, 9, 2),
                            ),
                        ],
                    ),
                    (
                        BrowseFilterablePage(title="browse filterable 2"),
                        [
                            AbstractFilterPage(
                                title="child 1 of browse filterable 2",
                                date_published=dt.date(2016, 9, 3),
                            ),
                        ],
                    ),
                ],
            )
        ]

    def setUp(self):
        self.request = RequestFactory().get("/")
        self.context = {"request": self.request}

    def test_get_appropriate_descendants(self):
        """
        Check to make sure the descendants of the sublanding page are the
        correct children that we saved during setup. The order of the
        retrieval should be consistent with the order in which they were saved.
        """

        descendants = self.page_tree[0].get_appropriate_descendants()
        self.assertEqual(descendants[0].title, "sublanding")
        self.assertEqual(descendants[1].title, "browse filterable 1")
        self.assertEqual(
            descendants[2].title, "child 1 of browse filterable 1"
        )
        self.assertEqual(
            descendants[3].title, "child 2 of browse filterable 1"
        )
        self.assertEqual(descendants[4].title, "browse filterable 2")

    def test_get_browsefilterable_posts(self):
        """
        Test to make sure the browsefilterable posts are retrieved correctly.
        The posts should be retrieved in reverse chronological order, and if
        the limit exceeds the total number of posts, all should be retrieved.
        """
        posts = self.page_tree[0].get_browsefilterable_posts(self.context, 3)
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0]["title"], "child 1 of browse filterable 2")
        self.assertEqual(posts[1]["title"], "child 2 of browse filterable 1")
        self.assertEqual(posts[2]["title"], "child 1 of browse filterable 1")

    def test_get_browsefilterable_posts_with_limit(self):
        """
        Same as the above test but imposes a limit that is smaller than the
        total number of posts. Check to make sure we only retrieve the
        specified number of posts, and that the most recent post comes first.
        """
        posts = self.page_tree[0].get_browsefilterable_posts(self.context, 1)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["title"], "child 1 of browse filterable 2")

    def test_render_post_preview_snapshot(self):
        response = self.page_tree[0].serve(self.request)
        self.assertContains(response, '<div class="o-post-preview__content">')

        for url, title in [
            (
                "browse-filterable-2/child-1-of-browse-filterable-2/",
                "child 1 of browse filterable 2",
            ),
            (
                "browse-filterable-1/child-2-of-browse-filterable-1/",
                "child 2 of browse filterable 1",
            ),
            (
                "browse-filterable-1/child-1-of-browse-filterable-1/",
                "child 1 of browse filterable 1",
            ),
        ]:
            self.assertContains(
                response,
                (
                    '<h3 class="o-post-preview__title">'
                    f'<a href="/sublanding/{url}">{title}</a>'
                    "</h3>"
                ),
                html=True,
            )


class TestSublandingPageHasHero(SimpleTestCase):
    def test_no_hero(self):
        self.assertFalse(SublandingPage().has_hero)

    def test_has_hero(self):
        self.assertTrue(
            SublandingPage(
                header=json.dumps(
                    [{"type": "hero", "value": {"heading": "Heading"}}]
                )
            ).has_hero
        )
