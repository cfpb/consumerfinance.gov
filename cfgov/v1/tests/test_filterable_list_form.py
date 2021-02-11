import time
from datetime import datetime

from django.core import management
from django.test import TestCase, override_settings

from pytz import timezone

from v1.forms import FilterableListForm
from v1.models import BlogPage
from v1.models.base import CFGOVPageCategory
from v1.models.learn_page import AbstractFilterPage, EventPage
from v1.tests.wagtail_pages.helpers import publish_page
from v1.util.categories import clean_categories


@override_settings(ELASTICSEARCH_DSL_AUTOSYNC=True)
@override_settings(ELASTICSEARCH_DSL_AUTO_REFRESH=True)
class TestFilterableListForm(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        # Create a clean index for the test suite
        management.call_command('search_index', action='delete', force=True, models=['v1'])
        management.call_command('search_index', action='create', models=['v1'])

        blog1 = BlogPage(title='test page')
        blog1.categories.add(CFGOVPageCategory(name='foo'))
        blog1.categories.add(CFGOVPageCategory(name='bar'))
        blog1.tags.add('foo')
        blog1.authors.add('richa-agarwal')
        blog1.authors.add('sarah-simpson')
        blog2 = BlogPage(title='another test page')
        blog2.categories.add(CFGOVPageCategory(name='bar'))
        blog2.tags.add('blah')
        blog2.authors.add('richard-cordray')
        event1 = EventPage(
            title='test page 2',
            start_dt=datetime.now(timezone('UTC'))
        )
        event1.tags.add('bar')
        cool_event = EventPage(
            title='Cool Event',
            start_dt=datetime.now(timezone('UTC'))
        )
        awesome_event = EventPage(
            title='Awesome Event',
            start_dt=datetime.now(timezone('UTC'))
        )
        publish_page(blog1)
        publish_page(blog2)
        publish_page(event1)
        publish_page(cool_event)
        publish_page(awesome_event)
        cls.blog1 = blog1
        cls.blog2 = blog2
        cls.event1 = event1
        cls.cool_event = cool_event
        cls.awesome_event = awesome_event
        time.sleep(2)
    
    @classmethod
    def tearDownTestData(cls):
        # Delete pages to remove them from the ES Index
        cls.blog1.delete()
        cls.blog2.delete()
        cls.event1.delete()
        cls.cool_event.delete()
        cls.awesome_event.delete()
    
    def setUpFilterableForm(self, data=None):
        filterable_pages = AbstractFilterPage.objects.live()
        form = FilterableListForm(
            filterable_pages=filterable_pages,
            wagtail_block=None,
            filterable_root='/',
            filterable_categories=None
        )
        form.is_bound = True
        form.cleaned_data = data
        return form

    def test_filter_by_category(self):
        form = self.setUpFilterableForm(data={'categories': ['foo']})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.blog1)

    def test_filter_by_nonexisting_category(self):
        form = self.setUpFilterableForm(data={'categories': ['test filter']})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 0)

    def test_filter_by_tags(self):
        form = self.setUpFilterableForm(data={'topics': ['foo', 'bar']})
        page_set_pks = form.get_page_set().values_list('pk', flat=True)
        self.assertEqual(len(page_set_pks), 2)
        self.assertIn(self.blog1.pk, page_set_pks)
        self.assertIn(self.event1.pk, page_set_pks)

    def test_filter_doesnt_return_drafts(self):
        page2 = BlogPage(title='test page 2')
        page2.tags.add('foo')
        # Don't publish new page
        form = self.setUpFilterableForm(data={'topics': ['foo']})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.blog1)

    def test_filter_by_author_names(self):
        form = self.setUpFilterableForm(data={'authors': ['sarah-simpson']})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.blog1)

    def test_filter_by_title(self):
        form = self.setUpFilterableForm(data={'title': 'Cool'})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.cool_event)

    def test_validate_date_after_1900_can_pass(self):
        form = self.setUpFilterableForm()
        form.data = {'from_date': '1/1/1900', 'archived': 'exclude'}
        self.assertTrue(form.is_valid())

    def test_validate_date_after_1900_can_fail(self):
        form = self.setUpFilterableForm()
        form.data = {'from_date': '12/31/1899'}
        self.assertFalse(form.is_valid())
        self.assertIn('from_date', form._errors)

    def test_clean_categories_converts_blog_subcategories_correctly(self):
        form = self.setUpFilterableForm()
        form.data = {'categories': ['blog']}
        clean_categories(selected_categories=form.data.get('categories'))
        self.assertEqual(
            form.data['categories'],
            [
                'blog',
                'at-the-cfpb',
                'directors-notebook',
                'policy_compliance',
                'data-research-reports',
                'info-for-consumers'
            ]
        )

    def test_clean_categories_converts_reports_subcategories_correctly(self):
        form = self.setUpFilterableForm()
        form.data = {'categories': ['research-reports']}
        clean_categories(selected_categories=form.data.get('categories'))
        self.assertEqual(
            form.data['categories'],
            [
                'research-reports',
                'consumer-complaint',
                'super-highlight',
                'data-point',
                'industry-markets',
                'consumer-edu-empower',
                'to-congress',
            ]
        )


@override_settings(ELASTICSEARCH_DSL_AUTOSYNC=True)
@override_settings(ELASTICSEARCH_DSL_AUTO_REFRESH=True)
class TestFilterableListFormArchive(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a clean index for the test suite
        management.call_command('search_index', action='delete', force=True, models=['v1'])
        management.call_command('search_index', action='create', models=['v1'])

        page1 = BlogPage(title='test page', is_archived='yes')
        page2 = BlogPage(title='another test page')
        page3 = BlogPage(title='never-archived page', is_archived='never')
        publish_page(page1)
        publish_page(page2)
        publish_page(page3)
        cls.page1 = page1
        cls.page2 = page2
        cls.page3 = page3
        time.sleep(2)

    @classmethod
    def tearDownTestData(cls):
        cls.page1.delete()
        cls.page2.delete()
        cls.page3.delete()

    def setUpFilterableForm(self, data=None):
        filterable_pages = AbstractFilterPage.objects.live()
        form = FilterableListForm(
            filterable_pages=filterable_pages,
            wagtail_block=None,
            filterable_root='/',
            filterable_categories=None
        )
        form.is_bound = True
        form.cleaned_data = data
        return form

    def test_filter_by_archived_all(self):
        form = self.setUpFilterableForm()
        form.data = {}
        form.full_clean()
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 3)

    def test_filter_by_archived_include(self):
        form = self.setUpFilterableForm()
        form.data = {'archived': 'include'}
        form.full_clean()
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 3)

    def test_filter_by_archived_exclude(self):
        form = self.setUpFilterableForm()
        form.data = {'archived': 'exclude'}
        form.full_clean()
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 2)
        self.assertEqual(page_set[0].specific, self.page2)

    def test_filter_by_archived_only(self):
        form = self.setUpFilterableForm()
        form.data = {'archived': 'only'}
        form.full_clean()
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.page1)
