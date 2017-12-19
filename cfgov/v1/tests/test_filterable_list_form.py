from django.test import TestCase

from wagtail.wagtailcore.models import Site

from v1.forms import FilterableListForm
from v1.models import BlogPage
from v1.models.base import CFGOVPageCategory
from v1.models.learn_page import AbstractFilterPage, EventPage
from v1.tests.wagtail_pages.helpers import publish_page
from v1.util.categories import clean_categories


class TestFilterableListForm(TestCase):

    def setUpFilterableForm(self, data=None):
        base_query = AbstractFilterPage.objects.live()
        form = FilterableListForm(base_query=base_query)
        form.is_bound = True
        form.cleaned_data = data
        return form

    def test_filter_by_category(self):
        page1 = BlogPage(title='test page')
        page1.categories.add(CFGOVPageCategory(name='foo'))
        page1.categories.add(CFGOVPageCategory(name='bar'))
        page2 = BlogPage(title='another test page')
        page2.categories.add(CFGOVPageCategory(name='bar'))
        publish_page(page1)
        publish_page(page2)
        form = self.setUpFilterableForm(data={'categories': ['foo']})
        page_set = form.get_page_set()
        self.assertEquals(len(page_set), 1)
        self.assertEquals(page_set[0].specific, page1)

    def test_filter_by_nonexisting_category(self):
        form = self.setUpFilterableForm(data={'categories': ['made up filter']})
        page_set = form.get_page_set()
        self.assertEquals(len(page_set), 0)

    def test_filter_by_tags(self):
        page1 = BlogPage(title='test page 1')
        page1.tags.add('foo')
        page2 = EventPage(title='test page 2')
        page2.tags.add('bar')
        page3 = BlogPage(title='test page 3')
        page3.tags.add('blah')
        publish_page(page1)
        publish_page(page2)
        publish_page(page3)
        form = self.setUpFilterableForm(data={'topics': ['foo', 'bar']})
        page_set_pks = form.get_page_set().values_list('pk', flat=True)
        self.assertEquals(len(page_set_pks), 2)
        self.assertIn(page1.pk, page_set_pks)
        self.assertIn(page2.pk, page_set_pks)

    def test_filter_doesnt_return_drafts(self):
        page1 = BlogPage(title='test page 1')
        page1.tags.add('foo')
        page2 = BlogPage(title='test page 2')
        page2.tags.add('foo')
        publish_page(page1)  # Only publish one of the pages
        form = self.setUpFilterableForm(data={'topics': ['foo']})
        page_set = form.get_page_set()
        self.assertEquals(len(page_set), 1)
        self.assertEquals(page_set[0].specific, page1)

    def test_filter_by_author_names(self):
        page1 = BlogPage(title='test page 1')
        page1.authors.add('richa-agarwal')
        page1.authors.add('sarah-simpson')
        page2 = BlogPage(title='test page 2')
        page2.authors.add('richard-cordray')
        publish_page(page1)
        publish_page(page2)
        form = self.setUpFilterableForm(data={'authors': ['sarah-simpson']})
        page_set = form.get_page_set()
        self.assertEquals(len(page_set), 1)
        self.assertEquals(page_set[0].specific, page1)

    def test_filter_by_title(self):
        page1 = EventPage(title='Cool Event')
        page2 = EventPage(title='Awesome Event')
        publish_page(page1)
        publish_page(page2)
        form = self.setUpFilterableForm(data={'title': 'Cool'})
        page_set = form.get_page_set()
        self.assertEquals(len(page_set), 1)
        self.assertEquals(page_set[0].specific, page1)

    def test_clean_categories_converts_blog_subcategories_correctly(self):
        form = self.setUpFilterableForm()
        form.data = {'categories': ['blog']}
        clean_categories(selected_categories=form.data.get('categories'))
        self.assertEquals(form.data['categories'], ['blog', 'at-the-cfpb', 'policy_compliance', 'data-research-reports', 'info-for-consumers'])

    def test_clean_categories_converts_reports_subcategories_correctly(self):
        form = self.setUpFilterableForm()
        form.data = {'categories': ['research-reports']}
        clean_categories(selected_categories=form.data.get('categories'))
        self.assertEquals(form.data['categories'], ['research-reports', 'consumer-complaint', 'super-highlight', 'data-point', 'industry-markets', 'consumer-edu-empower', 'to-congress'])
