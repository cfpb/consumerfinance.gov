import json
from datetime import datetime
from io import StringIO

from django.test import TestCase

from wagtail.core.models import Site

import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone

from search.elasticsearch_helpers import rebuild_elasticsearch_index
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch, FilterablePagesDocument,
    FilterablePagesDocumentSearch
)
from v1.models.base import CFGOVPageCategory
from v1.models.blog_page import BlogPage
from v1.models.enforcement_action_page import (
    EnforcementActionPage, EnforcementActionStatus
)
from v1.models.learn_page import AbstractFilterPage, EventPage
from v1.tests.wagtail_pages.helpers import publish_page


class FilterablePagesDocumentTest(TestCase):

    def test_model_class_added(self):
        self.assertEqual(FilterablePagesDocument.django.model, AbstractFilterPage)

    def test_ignore_signal_default(self):
        self.assertFalse(FilterablePagesDocument.django.ignore_signals)

    def test_auto_refresh_default(self):
        self.assertFalse(FilterablePagesDocument.django.auto_refresh)

    def test_fields_populated(self):
        mapping = FilterablePagesDocument._doc_type.mapping
        self.assertCountEqual(
            mapping.properties.properties.to_dict().keys(),
            [
                'tags', 'categories', 'authors', 'title', 'url',
                'is_archived', 'date_published', 'start_dt', 'end_dt',
                'statuses', 'initial_filing_date'
            ]
        )

    def test_get_queryset(self):
        test_event = EventPage(
            title="Testing",
            start_dt=datetime.now(timezone('UTC'))
        )
        qs = FilterablePagesDocument().get_queryset()
        self.assertFalse(qs.filter(title=test_event.title).exists())

    def test_prepare_statuses(self):
        enforcement = EnforcementActionPage(
            title="Great Test Page",
            preview_description='This is a great test page.',
            initial_filing_date=datetime.now(timezone('UTC'))
        )
        status = EnforcementActionStatus(status='expired-terminated-dismissed')
        enforcement.statuses.add(status)
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(enforcement)
        self.assertEqual(prepared_data['statuses'], ['expired-terminated-dismissed'])


class FilterablePagesDocumentSearchTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.site = Site.objects.get(is_default_site=True)
        event = EventPage(
            title='Event Test',
            start_dt=datetime(2021, 2, 16, tzinfo=timezone('UTC')),
            end_dt=datetime(2021, 2, 16, tzinfo=timezone('UTC'))
        )
        event.tags.add('test-topic')
        event.categories.add(CFGOVPageCategory(name='test-category'))
        event.authors.add('test-author')
        publish_page(event)
        enforcement = EnforcementActionPage(
            title="Great Test Page",
            preview_description='This is a great test page.',
            initial_filing_date=datetime.now(timezone('UTC'))
        )
        status = EnforcementActionStatus(status='expired-terminated-dismissed')
        enforcement.statuses.add(status)
        publish_page(enforcement)
        blog = BlogPage(
            title="Blog Page"
        )
        publish_page(blog)
        cls.event = event
        cls.enforcement = enforcement
        cls.blog = blog

        rebuild_elasticsearch_index('v1', stdout=StringIO())

    def test_search_event_all_fields(self):
        to_date_dt = datetime(2021, 3, 16)
        to_date = datetime.date(to_date_dt)
        from_date_dt = datetime(2021, 1, 16)
        from_date = datetime.date(from_date_dt)

        results = EventFilterablePagesDocumentSearch(
            prefix='/',
            topics=['test-topic'],
            categories=['test-category'],
            authors=['test-author'],
            to_date=to_date,
            from_date=from_date,
            title='Event Test',
            archived=['no']).search()
        self.assertTrue(results.filter(title=self.event.title).exists())

    def test_search_blog_dates(self):
        to_date_dt = datetime.today() + relativedelta(months=1)
        to_date = datetime.date(to_date_dt)
        from_date_dt = datetime.today() - relativedelta(months=1)
        from_date = datetime.date(from_date_dt)

        results = FilterablePagesDocumentSearch(
            prefix='/',
            topics=[],
            categories=[],
            authors=[],
            to_date=to_date,
            from_date=from_date,
            title=None,
            archived=None).search()
        self.assertTrue(results.filter(title=self.blog.title).exists())

    def test_search_enforcement_actions(self):
        to_date_dt = datetime.today() + relativedelta(months=1)
        to_date = datetime.date(to_date_dt)
        from_date_dt = datetime.today() - relativedelta(months=1)
        from_date = datetime.date(from_date_dt)

        results = EnforcementActionFilterablePagesDocumentSearch(
            prefix='/',
            topics=[],
            categories=[],
            authors=[],
            to_date=to_date,
            from_date=from_date,
            title=None,
            statuses=['expired-terminated-dismissed'],
            archived=None).search()
        self.assertTrue(results.filter(title=self.enforcement.title).exists())

    def test_search_enforcement_actions_no_statuses(self):
        to_date_dt = datetime.today() + relativedelta(months=1)
        to_date = datetime.date(to_date_dt)
        from_date_dt = datetime.today() - relativedelta(months=1)
        from_date = datetime.date(from_date_dt)

        results = EnforcementActionFilterablePagesDocumentSearch(
            prefix='/',
            topics=[],
            categories=[],
            authors=[],
            to_date=to_date,
            from_date=from_date,
            title=None,
            statuses=[],
            archived=None).search()
        self.assertTrue(results.filter(title=self.enforcement.title).exists())
