import datetime as dt
import re

from django.test import RequestFactory, TestCase

from wagtail.core.models import Page, Site

from pytz import timezone

from v1.atomic_elements.organisms import RelatedPosts
from v1.models.base import CFGOVPage, CFGOVPageCategory
from v1.models.blog_page import BlogPage
from v1.models.learn_page import EventPage
from v1.models.newsroom_page import NewsroomPage
from v1.tests.wagtail_pages import helpers


class RelatedPostsTestCase(TestCase):

    def setUp(self):

        # add some authors to a CFGOV page and give it some tags

        self.author1 = 'Some Author'
        self.author2 = 'Another Person'
        self.author3 = 'A Third Author'
        self.page_with_authors = CFGOVPage(title='a cfgov page with authors')
        helpers.save_new_page(self.page_with_authors)

        self.page_with_authors.authors.add(self.author1)
        self.page_with_authors.authors.add(self.author2)
        self.page_with_authors.authors.add(self.author3)

        self.page_with_authors.tags.add('tag 1')
        self.page_with_authors.tags.add('tag 2')

        # set up parent pages for the different types of related
        # posts we can have

        self.blog_parent = CFGOVPage(
            slug='blog', title='blog parent'
        )
        self.newsroom_parent = CFGOVPage(
            slug='newsroom', title='newsroom parent'
        )
        self.events_parent = CFGOVPage(
            slug='events', title='events parent'
        )
        self.archive_events_parent = CFGOVPage(
            slug='archive-past-events', title='archive past events parent'
        )
        self.activity_log = CFGOVPage(
            slug='activity-log', title='activity log'
        )

        helpers.save_new_page(self.blog_parent)
        helpers.save_new_page(self.newsroom_parent)
        helpers.save_new_page(self.events_parent)
        helpers.save_new_page(self.archive_events_parent)
        helpers.save_new_page(self.activity_log)

        # set up children of the parent pages and give them some tags
        # and some categories

        self.blog_child1 = BlogPage(
            title='blog child 1', date_published=dt.date(2016, 9, 1)
        )
        self.blog_child1.tags.add('tag 1')
        self.blog_child1.categories.add(
            CFGOVPageCategory(name='info-for-consumers')
        )

        self.blog_child2 = BlogPage(
            title='blog child 2', date_published=dt.date(2016, 9, 2)
        )
        self.blog_child2.tags.add('tag 2')
        self.blog_child2.categories.add(
            CFGOVPageCategory(name='policy_compliance')
        )

        self.newsroom_child1 = NewsroomPage(
            title='newsroom child 1', date_published=dt.date(2016, 9, 2)
        )
        self.newsroom_child1.tags.add('tag 1')
        self.newsroom_child1.tags.add('tag 2')
        self.newsroom_child1.categories.add(
            CFGOVPageCategory(name='op-ed')
        )

        self.newsroom_child2 = NewsroomPage(
            title='newsroom child 2', date_published=dt.date(2016, 9, 3)
        )
        self.newsroom_child2.tags.add('tag 2')
        self.newsroom_child2.categories.add(
            CFGOVPageCategory(name='some-other-category')
        )

        self.events_child1 = EventPage(
            title='events child 1',
            date_published=dt.date(2016, 9, 7),
            start_dt=dt.datetime.now(timezone('UTC'))
        )
        self.events_child1.tags.add('tag 1')

        self.events_child2 = EventPage(
            title='events child 2',
            date_published=dt.date(2016, 9, 5),
            start_dt=dt.datetime.now(timezone('UTC'))
        )
        self.events_child2.tags.add('tag 2')

        helpers.save_new_page(self.blog_child1, self.blog_parent)
        helpers.save_new_page(self.blog_child2, self.blog_parent)
        helpers.save_new_page(self.newsroom_child1, self.newsroom_parent)
        helpers.save_new_page(self.newsroom_child2, self.newsroom_parent)
        helpers.save_new_page(self.events_child1, self.events_parent)

        # mock a stream block that dictates how to retrieve the related posts
        # note that because of the way that the related_posts_category_lookup
        # function works i.e. by consulting a hard-coded object, the
        # specific_categories slot of the dict has to be something that it can
        # actually find.
        self.block_value = {
            'limit': 3,
            'show_heading': True,
            'header_title': 'Further reading',
            'relate_posts': False,
            'relate_newsroom': False,
            'relate_events': False,
            'specific_categories': [],
            'and_filtering': False,
        }

    def test_related_posts_blog(self):
        """
        Tests whether related posts from the blog from the supplied specific
        categories are retrieved. We expect there to be two such posts from
        the blog because we added two such posts in the setup. There should
        be no other posts in either of the other categories.
        """

        self.block_value['relate_posts'] = True
        self.block_value['relate_newsroom'] = False
        self.block_value['relate_events'] = False
        self.block_value['specific_categories'] = [
            'Info for Consumers', 'Policy &amp; Compliance'
        ]

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Blog', related_posts)
        self.assertEqual(len(related_posts['Blog']), 2)
        self.assertEqual(related_posts['Blog'][0], self.blog_child2)
        self.assertEqual(related_posts['Blog'][1], self.blog_child1)
        self.assertEqual(
            related_posts['Blog'][0].content_type.model, 'blogpage'
        )
        self.assertNotIn('Newsroom', related_posts)
        self.assertNotIn('Events', related_posts)

    def test_related_posts_blog_limit(self):
        """
        Tests whether related posts from the blog from the supplied specific
        categories are retrieved, subject to supplied limit. We expect there
        to be one such post from the blog, that post should be the one with
        the most recent publication date, and no other categories
        (newsroom, events) to have, any posts in them.
        """

        self.block_value['relate_posts'] = True
        self.block_value['relate_newsroom'] = False
        self.block_value['relate_events'] = False
        self.block_value['limit'] = 1
        self.block_value['specific_categories'] = [
            'Info for Consumers', 'Policy &amp; Compliance'
        ]

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Blog', related_posts)
        self.assertEqual(len(related_posts['Blog']), 1)
        self.assertEqual(related_posts['Blog'][0], self.blog_child2)
        self.assertNotIn('Newsroom', related_posts)
        self.assertNotIn('Events', related_posts)

    def test_related_posts_and_filtering_true(self):
        """
        Tests whether related posts are retrieved if the 'and_filtering' option
        is checked, and that the only posts retrieved match ALL of the tags on
        the calling page.
        """

        self.block_value['relate_posts'] = True
        self.block_value['relate_newsroom'] = True
        self.block_value['relate_events'] = True
        self.block_value['and_filtering'] = True

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertNotIn('Blog', related_posts)
        self.assertIn('Newsroom', related_posts)
        self.assertEqual(len(related_posts['Newsroom']), 1)
        self.assertEqual(related_posts['Newsroom'][0], self.newsroom_child1)
        self.assertNotIn('Events', related_posts)

    def test_related_posts_and_filtering_false(self):
        """
        Tests whether related posts are retrieved if, when the 'and_filtering'
        option is not checked, they match at least one of the tags on the
        calling page.
        """

        self.block_value['relate_posts'] = True
        self.block_value['and_filtering'] = False

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Blog', related_posts)
        self.assertEqual(len(related_posts['Blog']), 2)
        self.assertEqual(related_posts['Blog'][0], self.blog_child2)
        self.assertEqual(related_posts['Blog'][1], self.blog_child1)

    def test_related_posts_newsroom(self):
        """
        Tests whether related posts from the newsroom for the supplied specific
        categories are retrieved. We expect there to be one such post from
        the newsroom; we added two newsroom children but one of them should not
        match. We also expect that no other categories (newsroom, events) have
        any posts in them.
        """

        self.block_value['relate_posts'] = False
        self.block_value['relate_newsroom'] = True
        self.block_value['relate_events'] = False
        self.block_value['specific_categories'] = ['Op-Ed']

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Newsroom', related_posts)
        self.assertEqual(len(related_posts['Newsroom']), 1)
        self.assertEqual(related_posts['Newsroom'][0], self.newsroom_child1)
        self.assertEqual(
            related_posts['Newsroom'][0].content_type.model, 'newsroompage'
        )
        self.assertNotIn('Blog', related_posts)
        self.assertNotIn('Events', related_posts)

    def test_related_posts_events(self):
        """
        Tests whether related posts from events are retrieved. Events have
        no specific categories associated with them so it doesn't matter what
        that value is set to. We expect there to be one such post from
        events because we added one child to the events parent. We also expect
        that no other categories (newsroom, blog) have any posts in them.
        """

        self.block_value['relate_posts'] = False
        self.block_value['relate_newsroom'] = False
        self.block_value['relate_events'] = True
        self.block_value['specific_categories'] = [
            'anything', 'can', 'be', 'here'
        ]

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Events', related_posts)
        self.assertEqual(len(related_posts), 1)
        self.assertEqual(related_posts['Events'][0], self.events_child1)
        self.assertEqual(
            related_posts['Events'][0].content_type.model, 'eventpage'
        )
        self.assertNotIn('Blog', related_posts)
        self.assertNotIn('Newsroom', related_posts)

    def test_related_posts_events_archive(self):
        """
        Tests whether related posts from archived events are retrieved.
        Events have no specific categories associated with them so it
        doesn't matter what that value is set to. Here, we save an
        archived event child, and thus we expect that we should retrieve
        both the original event child and the archive event child.
        We also expect that no other categories (newsroom, blog) have
        any posts in them.
        """
        helpers.save_new_page(self.events_child2, self.archive_events_parent)

        self.block_value['relate_posts'] = False
        self.block_value['relate_newsroom'] = False
        self.block_value['relate_events'] = True
        self.block_value['specific_categories'] = [
            'anything', 'can', 'be', 'here'
        ]

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Events', related_posts)
        self.assertEqual(len(related_posts['Events']), 2)
        self.assertNotIn('Blog', related_posts)
        self.assertNotIn('Newsroom', related_posts)
        self.assertEqual(related_posts['Events'][0], self.events_child1)
        self.assertEqual(related_posts['Events'][1], self.events_child2)

    def test_related_posts_all(self):
        """
        We test whether all the different posts are retrieved. This is
        basically the logical AND of the blog, newsroom, and events
        tests. We expect to retrieve all the blog, newsroom, and events
        posts (two, one, and one of each, respectively).
        """

        self.block_value['relate_posts'] = True
        self.block_value['relate_newsroom'] = True
        self.block_value['relate_events'] = True
        self.block_value['specific_categories'] = ['Info for Consumers',
                                                   'Policy &amp; Compliance',
                                                   'Op-Ed']

        related_posts = RelatedPosts.related_posts(
            self.page_with_authors,
            self.block_value
        )

        self.assertIn('Blog', related_posts)
        self.assertIn('Newsroom', related_posts)
        self.assertIn('Events', related_posts)

        self.assertEqual(len(related_posts['Blog']), 2)
        self.assertEqual(len(related_posts['Events']), 1)
        self.assertEqual(len(related_posts['Newsroom']), 1)

        self.assertEqual(related_posts['Blog'][0], self.blog_child2)
        self.assertEqual(related_posts['Blog'][1], self.blog_child1)
        self.assertEqual(related_posts['Events'][0], self.events_child1)
        self.assertEqual(related_posts['Newsroom'][0], self.newsroom_child1)

    def test_related_posts_rendering(self):
        block_value = {
            'and_filtering': False,
            'alternate_view_more_url': None,
            'limit': 3,
            'relate_events': True,
            'relate_newsroom': True,
            'relate_posts': True,
            'specific_categories': [],
        }

        context = {
            'page': self.page_with_authors,
            'request': RequestFactory().get('/'),
        }

        html = RelatedPosts().render(block_value, context=context)

        # Rendered HTML should contain 5 results, because the limit only
        # applies to each type of post, not the total number.
        self.assertEqual(len(re.findall('m-list_item', html)), 5)


class TestGenerateViewMoreUrl(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.root = Site.objects.first().root_page

    def _create_activity_log_page(self):
        activity_log = CFGOVPage(title='Activity log', slug='activity-log')
        self.root.add_child(instance=activity_log)

    def test_no_activity_log_page_raises_does_not_exist(self):
        page = CFGOVPage(title='test')
        self.root.add_child(instance=page)

        with self.assertRaises(Page.DoesNotExist):
            RelatedPosts.view_more_url(page, self.request)

    def test_no_tags_url_has_no_query_string(self):
        self._create_activity_log_page()

        page = CFGOVPage(title='test')
        self.root.add_child(instance=page)

        self.assertEqual(
            RelatedPosts.view_more_url(page, self.request),
            '/activity-log/'
        )

    def test_tags_get_appended_as_query_string(self):
        self._create_activity_log_page()

        page = CFGOVPage(title='test')
        self.root.add_child(instance=page)
        page.tags.add('bar')
        page.tags.add('foo')

        self.assertEqual(
            RelatedPosts.view_more_url(page, self.request),
            '/activity-log/?topics=bar&topics=foo'
        )
