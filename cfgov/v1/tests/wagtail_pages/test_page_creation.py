from django.test import Client, TestCase
from django.core.exceptions import ValidationError

from v1.tests.wagtail_pages.helpers import (
    create_landing_page,
    create_sublanding_filterable_page,
    create_blog_page,
)

class PageCreationTestCase(TestCase):

    def test_landing_page_does_not_exist(self):
        """landing page should be created if it does not exist"""
        create_landing_page("About us", "about-us")

        www_response = Client.get('/about-us/')
        self.assertEqual(www_response.status_code, 200)

    def test_landing_page_exists_fail(self):
        """page creation should abort if it already exists, returns none"""
        path = create_landing_page("About us", "about-us")
        self.assertIsNone(path)

    def test_sublanding_page_with_blog_as_child(self):
        """blog page should be created as child of sublanding page"""
        path = create_sublanding_filterable_page("blog", "blog")
        new_path = create_blog_page("post1", "post1", path)
        self.assertIn("/blog/post1", new_path)