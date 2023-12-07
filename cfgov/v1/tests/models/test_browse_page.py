from django.test import RequestFactory, TestCase

from wagtail.models import Site

from v1.models import BrowseFilterablePage, BrowsePage, CFGOVPage


class TestSecondaryNav(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.site_root = Site.objects.get(is_default_site=True).root_page

        # Create a tree structure like:
        # -
        # -- browse1
        # --- browsechild1
        # -- browse2
        # --- browsechild2
        self.browse1 = BrowsePage(title="Browse 1", live=True)
        self.site_root.add_child(instance=self.browse1)

        self.browsechild1 = BrowsePage(title="Browse child 1", live=True)
        self.browse1.add_child(instance=self.browsechild1)

        self.browse2 = BrowsePage(title="Browse 2", live=True)
        self.site_root.add_child(instance=self.browse2)

        self.browsechild2 = BrowsePage(title="Browse child 2", live=True)
        self.browse2.add_child(instance=self.browsechild2)

    def test_nav_includes_sibling_browse_pages(self):
        nav = self.browse1.get_secondary_nav_items(self.request)

        self.assertEqual(len(nav), 2)
        self.assertEqual(nav[0]["title"], "Browse 1")
        self.assertEqual(nav[1]["title"], "Browse 2")

    def test_nav_secondary_nav_exclude_sibling_pages(self):
        self.browse1.secondary_nav_exclude_sibling_pages = True
        nav = self.browse1.get_secondary_nav_items(self.request)

        self.assertEqual(len(nav), 1)
        self.assertEqual(nav[0]["title"], "Browse 1")

    def test_nav_includes_browse_filterable_sibling_pages(self):
        browse_filterable = BrowseFilterablePage(
            title="Browse filterable", live=True
        )
        self.site_root.add_child(instance=browse_filterable)

        nav = self.browse1.get_secondary_nav_items(self.request)

        self.assertEqual(len(nav), 3)
        self.assertEqual(nav[0]["title"], "Browse 1")
        self.assertEqual(nav[1]["title"], "Browse 2")
        self.assertEqual(nav[2]["title"], "Browse filterable")

    def test_nav_does_not_include_non_browse_type_sibling_pages(self):
        non_browse = CFGOVPage(title="Non-browse page", live=True)
        self.site_root.add_child(instance=non_browse)

        nav = self.browse1.get_secondary_nav_items(self.request)

        self.assertEqual(len(nav), 2)
        self.assertEqual(nav[0]["title"], "Browse 1")
        self.assertEqual(nav[1]["title"], "Browse 2")

    def test_nav_for_browse_page_includes_only_its_children(self):
        nav = self.browse1.get_secondary_nav_items(self.request)

        self.assertEqual(len(nav), 2)

        self.assertEqual(nav[0]["title"], "Browse 1")
        self.assertEqual(len(nav[0]["children"]), 1)
        self.assertEqual(nav[0]["children"][0]["title"], "Browse child 1")

        self.assertEqual(nav[1]["title"], "Browse 2")
        self.assertFalse(nav[1].get("children"))

    def test_nav_for_child_of_browse_page(self):
        nav = self.browsechild2.get_secondary_nav_items(self.request)

        self.assertEqual(len(nav), 2)

        self.assertEqual(nav[0]["title"], "Browse 1")
        self.assertFalse(nav[0].get("children"))

        self.assertEqual(nav[1]["title"], "Browse 2")
        self.assertEqual(len(nav[1]["children"]), 1)
        self.assertEqual(nav[1]["children"][0]["title"], "Browse child 2")
