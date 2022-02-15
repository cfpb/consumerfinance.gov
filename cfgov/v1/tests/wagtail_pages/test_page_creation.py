from django.test import Client, TestCase

from v1.tests.wagtail_pages.helpers import (
    create_landing_page,
    create_sublanding_filterable_page,
    create_blog_page,
    create_browse_filterable_page,
    create_learn_page,
    create_sublanding_page,
    create_browse_page,
)

class PageCreationTestCase(TestCase):

    def test_landing_page_does_not_exist(self):
        """landing page should be created if it does not exist"""
        create_landing_page("Test landing", "test-landing")

        www_response = Client.get('/test-landing/')
        self.assertEqual(www_response.status_code, 200)

    def test_landing_page_exists_fail(self):
        """page creation should abort if it already exists, returns none"""
        path = create_landing_page("Test landing", "test-landing")
        self.assertIsNone(path)

    def test_sublanding_page_with_blog_as_child(self):
        """blog page should be created as child of sublanding page"""
        path = create_sublanding_filterable_page("Test sublanding", "test-sublanding")
        new_path = create_blog_page("Test post1", "test-post1", path)
        self.assertIn("/test-sublanding/test-post1", new_path)

    def test_browse_filterable_page_with_learn_page_as_child(self):
        """learn page should be created as child of browse filterable page"""
        path = create_browse_filterable_page("Test browse filterable", "test-browse-filterable")
        new_path = create_learn_page("Test browse1", "test-browse1", path)
        self.assertIn("/test-browse-filterable/test-browse1", new_path)

    def test_landing_page_with_sublanding_page_as_child(self):
        """sublanding page should be created as child of landing page"""
        path = create_landing_page("Test landing 2", "test-landing2")
        new_path = create_sublanding_page("Test sublanding 2", "test-sublanding2", path)
        self.assertIn("/test-landing2/test-sublanding2", new_path)

    def test_browse_filterable_page_with_browse_page_as_child(self):
        """browse page should be created as child of browse filterable page"""
        path = create_browse_filterable_page("Test browse filterable 2", "test-browse-filterable2")
        new_path = create_browse_page("Test browse", "test-browse", path)
        self.assertIn("/test-browse-filterable2/test-browse", new_path)