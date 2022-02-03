from datetime import date
from unittest import mock

from django.test import TestCase

from v1.models import BrowseFilterablePage, BrowsePage, CFGOVPage, HomePage
from v1.tests.wagtail_pages import helpers
from v1.util import util


class TestUtilFunctions(TestCase):

    @mock.patch('__builtin__.isinstance')
    @mock.patch('__builtin__.vars')
    @mock.patch('v1.util.util.StreamValue')
    def get_streamfields_returns_dict_of_streamfields(
        self, mock_streamvalueclass, mock_vars, mock_isinstance
    ):
        page = mock.Mock()
        mock_vars.items.return_value = {'key': 'value'}
        mock_isinstance.return_value = True
        result = util.get_streamfields(page)
        self.assertEqual(result, {'key': 'value'})


class TestExtendedStrftime(TestCase):
    def test_date_formatted_without_leading_zero_in_day(self):
        test_date = date(2018, 4, 5)
        formatted_date = util.extended_strftime(test_date, '%b %_d, %Y')
        self.assertEqual(formatted_date, 'Apr 5, 2018')

    def test_date_formatted_with_custom_month_abbreviation(self):
        test_date = date(2018, 9, 5)
        formatted_date = util.extended_strftime(test_date, '%_m %d, %Y')
        self.assertEqual(formatted_date, 'Sept. 05, 2018')

    def test_date_formatted_with_default_pattern(self):
        test_date = date(2018, 9, 5)
        formatted_date = util.extended_strftime(test_date, '%b %d, %Y')
        self.assertEqual(formatted_date, 'Sep 05, 2018')


class TestSecondaryNav(TestCase):
    def setUp(self):
        self.request = mock.MagicMock()
        self.browse_page1 = BrowsePage(title='Browse page 1')
        self.browse_page2 = BrowsePage(title='Browse page 2')
        helpers.publish_page(child=self.browse_page1)
        helpers.publish_page(child=self.browse_page2)
        self.child_of_browse_page1 = BrowsePage(
            title='Child of browse page 1'
        )
        self.child_of_browse_page2 = BrowsePage(
            title='Child of browse page 2'
        )
        helpers.save_new_page(self.child_of_browse_page1, self.browse_page1)
        helpers.save_new_page(self.child_of_browse_page2, self.browse_page2)

    def test_nav_includes_sibling_browse_pages(self):
        nav, has_children = util.get_secondary_nav_items(
            self.request, self.browse_page1
        )
        self.assertEqual(nav[0]['title'], self.browse_page1.title)
        self.assertEqual(nav[1]['title'], self.browse_page2.title)

        self.assertEqual(len(nav), 2)

    def test_nav_includes_browse_filterable_sibling_pages(self):
        browse_filterable_page = BrowseFilterablePage(
            title='Browse filterable page'
        )
        helpers.publish_page(child=browse_filterable_page)

        nav, has_children = util.get_secondary_nav_items(
            self.request, self.browse_page1
        )

        self.assertEqual(len(nav), 3)
        self.assertEqual(nav[0]['title'], self.browse_page1.title)
        self.assertEqual(nav[1]['title'], self.browse_page2.title)
        self.assertEqual(nav[2]['title'], browse_filterable_page.title)

    def test_nav_does_not_include_non_browse_type_sibling_pages(self):
        non_browse_page = CFGOVPage(title='Non-browse page')
        helpers.publish_page(child=non_browse_page)

        nav, has_children = util.get_secondary_nav_items(
            self.request, self.browse_page1
        )

        self.assertEqual(len(nav), 2)

    def test_nav_for_browse_page_includes_only_its_children(self):
        nav, has_children = util.get_secondary_nav_items(
            self.request, self.browse_page1
        )

        self.assertEqual(len(nav), 2)

        self.assertEqual(nav[0]['title'], self.browse_page1.title)
        self.assertEqual(len(nav[0]['children']), 1)
        self.assertEqual(
            nav[0]['children'][0]['title'],
            self.child_of_browse_page1.title
        )

        self.assertEqual(nav[1]['title'], self.browse_page2.title)
        self.assertEqual(nav[1]['children'], [])

    def test_nav_for_child_of_browse_page_includes_only_children_of_parent_browse_page(self):  # noqa: E501
        nav, has_children = util.get_secondary_nav_items(
            self.request, self.child_of_browse_page2
        )

        self.assertEqual(len(nav), 2)

        self.assertEqual(nav[0]['title'], self.browse_page1.title)
        self.assertEqual(nav[0]['children'], [])

        self.assertEqual(nav[1]['title'], self.browse_page2.title)
        self.assertEqual(len(nav[1]['children']), 1)
        self.assertEqual(
            nav[1]['children'][0]['title'],
            self.child_of_browse_page2.title
        )

    def test_has_children_is_true_for_browse_page_with_browse_child(self):
        nav, has_children = util.get_secondary_nav_items(
            self.request, self.browse_page1
        )

        self.assertEqual(has_children, True)

    def test_has_children_is_true_for_browse_page_with_browse_filterable_child(self):  # noqa: E501
        browse_filterable_page = BrowsePage(title='Non-browse page')
        helpers.publish_page(child=browse_filterable_page)
        browse_filterable_page_child = BrowseFilterablePage(
            title='Child of non-browse page'
        )
        helpers.save_new_page(
            browse_filterable_page_child, browse_filterable_page
        )
        nav, has_children = util.get_secondary_nav_items(
            self.request, browse_filterable_page
        )

        self.assertEqual(has_children, True)

    def test_has_children_is_false_for_browse_page_with_only_non_browse_children(self):  # noqa: E501
        browse_page3 = BrowsePage(title='Browse page 3')
        helpers.publish_page(child=browse_page3)
        child_of_browse_page3 = CFGOVPage(
            title='Non-browse child of browse page'
        )
        helpers.save_new_page(child_of_browse_page3, browse_page3)

        nav, has_children = util.get_secondary_nav_items(
            self.request, browse_page3
        )

        self.assertEqual(has_children, False)

    def test_has_children_is_false_for_browse_page_with_no_children(self):
        browse_page_without_children = BrowsePage(
            title='Browse page without children'
        )
        helpers.publish_page(child=browse_page_without_children)

        nav, has_children = util.get_secondary_nav_items(
            self.request, browse_page_without_children
        )

        self.assertEqual(has_children, False)


class TestGetPageFromPath(TestCase):
    def test_no_root_returns_correctly(self):
        page = CFGOVPage(title='Test page')
        helpers.save_new_page(page)

        self.assertEqual(util.get_page_from_path('/test-page/'), page)

    def test_with_root_returns_correctly(self):
        page = CFGOVPage(title='Test page 2')
        helpers.save_new_page(page)
        root = HomePage.objects.get(title='CFGov')

        self.assertEqual(util.get_page_from_path('/test-page-2/', root), page)

    def test_bad_path_returns_correctly(self):
        self.assertEqual(util.get_page_from_path('/does-not-exist/'), None)
