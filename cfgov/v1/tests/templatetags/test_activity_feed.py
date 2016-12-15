import datetime
from unittest import TestCase

from wagtail.wagtailcore.models import Site

from v1.models import BlogPage
from v1.models.base import CFGOVPageCategory
from v1.templatetags import activity_feed
from v1.tests.wagtail_pages.helpers import publish_page


class TestActivityFeed(TestCase):


    def test_get_latest_activities_returns_relevant_activities(self):
        hostname = Site.objects.get(is_default_site=True).hostname
        page1 = BlogPage(title='test page')
        # Give it a blog subcategory
        page1.categories.add(CFGOVPageCategory(name='at-the-cfpb'))
        publish_page(page1)

        page2 = BlogPage(title='another test page')
        # Don't give it a blog subcategory
        publish_page(page2)

        activities = activity_feed.get_latest_activities(activity_type='blog', hostname=hostname) 
        self.assertEquals(len(activities), 1)
        self.assertEquals(activities[0].specific, page1)


    def test_get_latest_activities_returns_activities_sorted(self):
        hostname = Site.objects.get(is_default_site=True).hostname
        page1 = BlogPage(title='oldest page', date_published=datetime.date(2015, 9, 3))
        # Give it a newsroom subcategory
        page1.categories.add(CFGOVPageCategory(name='press-release'))
        publish_page(page1)

        page2 = BlogPage(title='second page', date_published=datetime.date(2016, 5, 3))
        # Give it a newsroom subcategory
        page2.categories.add(CFGOVPageCategory(name='speech'))
        publish_page(page2)

        page3 = BlogPage(title='most recent page')
        # Give it a newsroom subcategory
        page3.categories.add(CFGOVPageCategory(name='testimony'))
        publish_page(page3)

        activities = activity_feed.get_latest_activities(activity_type='newsroom', hostname=hostname) 
        self.assertEquals(len(activities), 3)
        self.assertEquals(activities[0].specific, page3)
        self.assertEquals(activities[1].specific, page2)
        self.assertEquals(activities[2].specific, page1)
