import datetime as dt
from unittest import TestCase

import mock
from wagtail.wagtailcore.blocks import StreamValue

import scripts._atomic_helpers as atomic
from v1.models import AbstractFilterPage, BrowseFilterablePage, SublandingPage
from v1.tests.wagtail_pages import helpers


class SublandingPageTestCase(TestCase):
    """
    This test case checks that the browse-filterable posts of a sublanding
    page are properly retrieved.
    """
    def setUp(self):
        self.request = mock.MagicMock()
        self.request.site.hostname = 'localhost:8000'
        self.limit = 10
        self.sublanding_page = SublandingPage(title='title')

        helpers.publish_page(child=self.sublanding_page)
        self.post1 = BrowseFilterablePage(title='post 1')
        self.post2 = BrowseFilterablePage(title='post 2')
        # the content of this post has both a full_width_text
        # and a filter_controls
        self.post1.content = StreamValue(self.post1.content.stream_block,
                                         [atomic.full_width_text, atomic.filter_controls],
                                         True)
        # this one only has a filter_controls
        self.post2.content = StreamValue(self.post1.content.stream_block,
                                         [atomic.filter_controls], True)

        helpers.save_new_page(self.post1, self.sublanding_page)
        helpers.save_new_page(self.post2, self.sublanding_page)

        # manually set the publication date of the posts to ensure consistent
        # order of retrieval in test situations, otherwise the `date_published`
        # can vary due to commit order

        self.child1_of_post1 = AbstractFilterPage(title='child 1 of post 1',
                                                  date_published=dt.date(2016, 9, 1))
        self.child2_of_post1 = AbstractFilterPage(title='child 2 of post 1',
                                                  date_published=dt.date(2016, 9, 2))
        self.child1_of_post2 = AbstractFilterPage(title='child 1 of post 2',
                                                  date_published=dt.date(2016, 9, 3))
        helpers.save_new_page(self.child1_of_post1, self.post1)
        helpers.save_new_page(self.child2_of_post1, self.post1)
        helpers.save_new_page(self.child1_of_post2, self.post2)

    def tearDown(self):

        pass

    def test_get_appropriate_descendants(self):
        """
        Check to make sure the descendants of the sublanding page are the
        correct children that we saved during setup. The order of the
        retrieval should be consistent with the order in which they were saved.
        """

        descendants = self.sublanding_page.get_appropriate_descendants(self.request.site.hostname)
        self.assertEqual(descendants[0].title, self.sublanding_page.title)
        self.assertEqual(descendants[1].title, self.post1.title)
        self.assertEqual(descendants[2].title, self.child1_of_post1.title)
        self.assertEqual(descendants[3].title, self.child2_of_post1.title)
        self.assertEqual(descendants[4].title, self.post2.title)

    def test_get_browsefilterable_posts(self):
        """
        Test to make sure the browsefilterable posts are retrieved correctly.
        The posts should be retrieved in reverse chronological order, and if
        the limit exceeds the total number of posts, all should be retrieved.
        """
        browsefilterable_posts = self.sublanding_page.get_browsefilterable_posts(self.request, self.limit)
        self.assertEqual(len(browsefilterable_posts), 3)
        # the first number in the tuple represents the order of the
        # filter_controls form in the post's content field, so we test
        # situations in which that order varies
        self.assertEqual(('1', self.child1_of_post1), browsefilterable_posts[2])
        self.assertEqual(('1', self.child2_of_post1), browsefilterable_posts[1])
        self.assertEqual(('0', self.child1_of_post2), browsefilterable_posts[0])

    def test_get_browsefilterable_posts_with_limit(self):
        """
        Same as the above test but imposes a limit that is smaller than the
        total number of posts. Check to make sure we only retrieve the
        specified number of posts, and that the most recent post comes first.
        """
        self.limit = 1
        browsefilterable_posts = self.sublanding_page.get_browsefilterable_posts(self.request, self.limit)
        self.assertEqual(1, len(browsefilterable_posts))
        self.assertEqual(('0', self.child1_of_post2), browsefilterable_posts[0])
