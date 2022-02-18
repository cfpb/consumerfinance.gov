from datetime import date

from django.test import Client, TestCase

from wagtail.core.models import Site

from v1.tests.wagtail_pages.helpers import (
    create_blog_page, create_browse_filterable_page, create_browse_page,
    create_landing_page, create_learn_page, create_sublanding_filterable_page,
    create_sublanding_page, get_parent_route
)


django_client = Client()


class PageCreationTestCase(TestCase):

    def test_landing_page_creation(self):
        """landing page should be created if it does not exist"""
        path = create_landing_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_landing_page_exists_fail(self):
        """landing page creation should abort if it already exists, \
            returns none"""
        create_landing_page("Test", "test")
        path = create_landing_page("Test", "test")
        self.assertIsNone(path)

    def test_sublanding_page_creation(self):
        """sublanding page should be created if it does not exist"""
        path = create_sublanding_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_sublanding_page_exists_fail(self):
        """sublanding page creation should abort if it already exists, \
            returns none"""
        create_sublanding_page("Test", "test")
        path = create_sublanding_page("Test", "test")
        self.assertIsNone(path)

    def test_sublanding_filterable_page_creation(self):
        """sublanding filterable page should be created if it \
            does not exist"""
        path = create_sublanding_filterable_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_sublanding_filterable_page_exists_fail(self):
        """sublanding filterable page creation should abort if it \
            already exists, returns none"""
        create_sublanding_filterable_page("Test", "test")
        path = create_sublanding_filterable_page("Test", "test")
        self.assertIsNone(path)

    def test_browse_filterable_page_creation(self):
        """browse filterable page should be created if it \
            does not exist"""
        path = create_browse_filterable_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_browse_filterable_page_exists_fail(self):
        """browse filterable page creation should abort if it \
            already exists, returns none"""
        create_browse_filterable_page("Test", "test")
        path = create_browse_filterable_page("Test", "test")
        self.assertIsNone(path)

    def test_browse_page_creation(self):
        """browse page should be created if it \
            does not exist"""
        path = create_browse_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_browse_page_exists_fail(self):
        """browse page creation should abort if it \
            already exists, returns none"""
        create_browse_page("Test", "test")
        path = create_browse_page("Test", "test")
        self.assertIsNone(path)

    def test_learn_page_creation(self):
        """learn page should be created if it \
            does not exist"""
        path = create_learn_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_learn_page_exists_fail(self):
        """learn page creation should abort if it \
            already exists, returns none"""
        create_learn_page("Test", "test")
        path = create_learn_page("Test", "test")
        self.assertIsNone(path)

    def test_blog_page_creation(self):
        """blog page should be created if it \
            does not exist"""
        path = create_blog_page("Test", "test")

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_blog_page_exists_fail(self):
        """blog page creation should abort if it \
            already exists, returns none"""
        create_blog_page("Test", "test")
        path = create_blog_page("Test", "test")
        self.assertIsNone(path)

    def test_sublanding_page_with_blog_as_child(self):
        """blog page should be created as child of sublanding page"""
        path = create_sublanding_filterable_page("Test", "test")
        new_path = create_blog_page("Test post", "test-post", path)
        self.assertIn("/test/test-post", new_path)

    def test_browse_filterable_page_with_learn_page_as_child(self):
        """learn page should be created as child of browse filterable page"""
        path = create_browse_filterable_page("Test", "test")
        new_path = create_learn_page("Test learn", "test-learn", path)
        self.assertIn("/test/test-learn", new_path)

    def test_landing_page_with_sublanding_page_as_child(self):
        """sublanding page should be created as child of landing page"""
        path = create_landing_page("Test", "test")
        new_path = create_sublanding_page("sublanding", "sublanding", path)
        self.assertIn("/test/sublanding", new_path)

    def test_browse_filterable_page_with_browse_page_as_child(self):
        """browse page should be created as child of browse filterable page"""
        path = create_browse_filterable_page("Test", "test")
        new_path = create_browse_page("Test browse", "test-browse", path)
        self.assertIn("/test/test-browse", new_path)

    def test_landing_page_with_optional_arguments(self):
        """landing page should be created correctly with one or more \
            optional arguments provided"""
        path = create_landing_page("Test", "test", None, True)

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_sublanding_page_with_optional_arguments(self):
        """sublanding page should be created correctly with one or more \
            optional arguments provided"""
        path = create_sublanding_page("Test", "test", None, True)

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_sublanding_filterable_page_with_optional_arguments(self):
        """sublanding filterable page should be created correctly with one \
            or more optional arguments provided"""
        path = create_sublanding_filterable_page("Test", "test", None, True)

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_browse_filterable_page_with_optional_arguments(self):
        """browse filterable page should be created correctly with one or \
            more optional arguments provided"""
        path = create_browse_filterable_page("Test", "test", None, True)

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_browse_page_with_optional_arguments(self):
        """browse page should be created correctly with one or more \
            optional arguments provided"""
        path = create_browse_page("Test", "test", None, True)

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_learn_page_with_optional_arguments(self):
        """learn page should be created correctly with one or more \
            optional arguments provided"""
        path = create_learn_page("Test", "test", None, {"test tag"},
                                 {"test category"}, date.today())

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_blog_page_with_optional_arguments(self):
        """blog page should be created correctly with one or more \
            optional arguments provided"""
        path = create_blog_page("Test", "test", None, {"test tag"},
                                {"test category"}, "es", date.today())

        www_response = django_client.get(path)
        self.assertEqual(www_response.status_code, 200)

    def test_path_does_not_exist_fail(self):
        """get parent root path fails when page does not exist"""
        site = Site.objects.get(is_default_site=True)
        path = get_parent_route(site, '/test-fake-path/')
        self.assertIsNone(path)

    def test_landing_path_does_not_exist_fail(self):
        """get landing path fails when parent path does not exist"""
        path = create_landing_page("Test", "test", '/test-fake-path/')
        self.assertIsNone(path)

    def test_sublanding_path_does_not_exist_fail(self):
        """get sublanding path fails when parent path does not exist"""
        path = create_sublanding_page("Test", "test", '/test-fake-path/')
        self.assertIsNone(path)

    def test_sublanding_filterable_path_does_not_exist_fail(self):
        """get sublanding filterable path fails when parent path does not \
            exist"""
        path = create_sublanding_filterable_page("Test", "test",
                                                 '/test-fake-path/')
        self.assertIsNone(path)

    def test_browse_filterable_path_does_not_exist_fail(self):
        """get browse filterable path fails when parent path does not \
            exist"""
        path = create_browse_filterable_page("Test", "test",
                                             '/test-fake-path/')
        self.assertIsNone(path)

    def test_browse_path_does_not_exist_fail(self):
        """get browse path fails when parent path does not exist"""
        path = create_browse_page("Test", "test", '/test-fake-path/')
        self.assertIsNone(path)

    def test_learn_path_does_not_exist_fail(self):
        """get learn path fails when parent path does not exist"""
        path = create_learn_page("Test", "test", '/test-fake-path/')
        self.assertIsNone(path)

    def test_blog_path_does_not_exist_fail(self):
        """get blog path fails when parent path does not exist"""
        path = create_blog_page("Test", "test", '/test-fake-path/')
        self.assertIsNone(path)

    def test_blog_page_with_none_optional_arguments(self):
        """blog page should be created correctly when None is provided as \
            optional arguments"""
        path = create_blog_page("Test", "test", None, None, None, None, None)
        self.assertIn("/test/", path)

    def test_learn_page_with_none_optional_arguments(self):
        """learn page should be created correctly when None is provided as \
            optional arguments"""
        path = create_learn_page("Test", "test", None, None, None, None)
        self.assertIn("/test/", path)
