from datetime import datetime

from django.test import TestCase

from wagtail.core.blocks import StreamValue

from pytz import timezone

from scripts._atomic_helpers import filter_controls as controls
from v1.atomic_elements.organisms import FilterableList
from v1.models import BlogPage, BrowseFilterablePage
from v1.models.learn_page import AbstractFilterPage, EventPage
from v1.tests.wagtail_pages import helpers


class TestFilterableList(TestCase):
    def alphabetical_topics(self):
        controls['value']['topic_filtering'] = 'sort_alphabetically'
        return controls

    def topics_by_frequency(self):
        controls['value']['topic_filtering'] = 'sort_by_frequency'
        return controls

    def set_up_published_pages(self):
        page1 = BlogPage(title='test page 1')
        page1.tags.add(u'C-tag-3-instances')

        page2 = EventPage(
            title='test page 2',
            start_dt=datetime.now(timezone('UTC'))
        )
        page2.tags.add(u'B-tag-2-instances')
        page2.tags.add(u'C-tag-3-instances')

        page3 = BlogPage(title='test page 3')
        page3.tags.add(u'A-tag-1-instance')
        page3.tags.add(u'B-tag-2-instances')
        page3.tags.add(u'C-tag-3-instances')

        helpers.publish_page(page1)
        helpers.publish_page(page2)
        helpers.publish_page(page3)

        filterable_pages = AbstractFilterPage.objects.live()
        self.page_ids = filterable_pages.values_list('id', flat=True)

    def set_up_filterable_list_page(self, value):
        self.page = BrowseFilterablePage(title='Browse filterable page')
        self.page.content = StreamValue(self.page.content.stream_block, [value], True)
        helpers.publish_page(child=self.page)
        self.block = self.page.get_filterable_list_wagtail_block()

    def test_get_filterable_topics_sort_by_frequency(self):
        self.set_up_filterable_list_page(self.topics_by_frequency())
        self.set_up_published_pages()
        topics = FilterableList().get_filterable_topics(self.page_ids, self.block.value)
        expected_topics = ['C-tag-3-instances', 'B-tag-2-instances', 'A-tag-1-instance']
        self.assertEqual([x[1] for x in topics], expected_topics)

    def test_get_filterable_topics_sort_alphabetically(self):
        self.set_up_filterable_list_page(self.alphabetical_topics())
        self.set_up_published_pages()
        topics = FilterableList().get_filterable_topics(self.page_ids, self.block.value)
        expected_topics = ['A-tag-1-instance', 'B-tag-2-instances', 'C-tag-3-instances']
        self.assertEqual([x[1] for x in topics], expected_topics)
