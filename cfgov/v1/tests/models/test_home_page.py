from django.test import TestCase

from v1.models import (
    BlogPage, EventPage, HomePage, NewsroomPage,
    SublandingFilterablePage,
)


class TestHomePage(TestCase):

    def setUp(self):
        self.home_page = HomePage.objects.get(slug='cfgov')

        # Set up a root for updates
        self.updates_page = SublandingFilterablePage(
            title='Updates', slug='updates', live=True
        )
        self.home_page.add_child(instance=self.updates_page)
        self.updates_page.save_revision().publish()

        # Set up blogs
        self.blog_1 = BlogPage(
            title='Blog 1', slug='blog1', live=True
        )
        self.blog_1.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.blog_1)
        self.blog_2 = BlogPage(
            title='Blog 2', slug='blog2', live=True
        )
        self.blog_2.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.blog_2)
        self.blog_3 = BlogPage(
            title='Blog 3', slug='blog3', live=True
        )
        self.blog_3.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.blog_3)

        # Set up some events
        self.event_1 = EventPage(
            title='Event 1', slug='event1', live=True
        )
        self.event_1.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.event_1)
        self.event_2 = EventPage(
            title='Event 2', slug='event2', live=True
        )
        self.event_2.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.event_2)
        self.event_3 = EventPage(
            title='Event 3', slug='event3', live=True
        )
        self.event_3.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.event_3)

        # Set up some Newsroom posts
        self.news_1 = NewsroomPage(
            title='Newsroom 1', slug='news1', live=True
        )
        self.news_1.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.news_1)
        self.news_2 = NewsroomPage(
            title='Newsroom 2', slug='news2', live=True
        )
        self.news_2.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.news_2)
        self.news_3 = NewsroomPage(
            title='Newsroom 3', slug='news3', live=True
        )
        self.news_3.categories.create(name='activity-log', page=self.blog_1)
        self.updates_page.add_child(instance=self.news_3)

        # Publish things in an order
        self.news_3.save_revision().publish()
        self.blog_2.save_revision().publish()
        self.event_2.save_revision().publish()
        self.blog_1.save_revision().publish()
        self.news_1.save_revision().publish()
        self.event_3.save_revision().publish()
        self.blog_3.save_revision().publish()
        self.event_1.save_revision().publish()
        self.news_2.save_revision().publish()

        # Set up some unpublished types
        self.unpublished_blog_1 = BlogPage(
            title='Unpublished blog 1', slug='unpublished_blog1', live=False
        )
        self.updates_page.add_child(instance=self.unpublished_blog_1)

        # Set up some events
        self.unpublished_event_1 = EventPage(
            title='Unpublished event 1', slug='unpublished_event1', live=False
        )
        self.updates_page.add_child(instance=self.unpublished_event_1)

        # Set up some Newsroom posts
        self.unpublished_news_1 = NewsroomPage(
            title='Unpublished news 1', slug='unpublished_news1', live=False
        )
        self.updates_page.add_child(instance=self.unpublished_news_1)

        # Add an excluded update to exclude event_1
        self.home_page.excluded_updates.create(
            page=self.home_page, excluded_page=self.event_1
        )
        self.home_page.save_revision().publish()

    def test_get_latest_updates(self):
        response = self.client.get('/')
        latest_updates = response.context_data['latest_updates']
        self.assertEqual(
            ['news2', 'blog3', 'event3', 'news1', 'blog1', 'event2'],
            [p.slug for p in latest_updates]
        )
