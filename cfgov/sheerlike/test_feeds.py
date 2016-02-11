import datetime

import mock
import feedparser
from django.test import TestCase
from django.test.client import RequestFactory

from sheerlike.feeds import SheerlikeFeed


class FakeESItem(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestRSSFeed(TestCase):

    @mock.patch('sheerlike.query.QueryResults')
    @mock.patch('sheerlike.feeds.QueryFinder')
    def test_successful_feed(self, mock_QueryFinder, mock_QueryResults):
        with mock.patch.object(SheerlikeFeed, 'get_settings') as mock_get_settings:
            with mock.patch.object(SheerlikeFeed, 'items') as mock_items:
                # Create some fake settings
                mock_get_settings.return_value = {"feed_title": "Test Feed",
                                                  "feed_url": "/test-url/",
                                                  "entry_title": "$$title$$",
                                                  "entry_author": "$$author$$",
                                                  "entry_content": "$$content$$",
                                                  "entry_summary": "$$excerpt$$",
                                                  "entry_url": "$$url$$",
                                                  "entry_updated": "$$modified$$"
                                                  }
                # Create some fake items to populate the feed
                fake_es_item_1 = FakeESItem(title='Hi, Sup',
                                            content='some content',
                                            url='/hi-sup/',
                                            author='Dan',
                                            modified=datetime.datetime.now())
                fake_es_item_2 = FakeESItem(title='Another Fine Title',
                                            content='interesting content',
                                            url='/another-fine-title/',
                                            author='Kurt',
                                            modified=datetime.datetime.now())
                # Ensure these are returned when SheerlikeFeed.items() is called
                mock_items.return_value = [fake_es_item_1, fake_es_item_2]
                self.feed = SheerlikeFeed()
                self.feed.doc_type = 'test'
                # In order to grab the feed results, we need to pass it a fake
                # request object
                rf = RequestFactory()
                get_request = rf.get('/feed/test-url/')
                f = feedparser.parse(self.feed.__call__(get_request).content)
                feed = f.feed
                entries = f.entries
                assert len(entries) == 2
                assert feed.title == 'Test Feed'
                for entry in entries:
                    if entry.author != 'Dan':
                        continue
                    assert entry.title == 'Hi, Sup'
                    assert entry.summary == 'some content'
                    assert entry.link == 'http://testserver/hi-sup/'
