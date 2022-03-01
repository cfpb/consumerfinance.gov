from datetime import date

from django.test import TestCase

from wagtail.core.models import Site

from model_bakery import baker
from taggit.models import Tag

from v1.models import BlogPage, CFGOVPageCategory
from v1.util.ref import categories
from v1.views.reports import PageMetadataReportView, process_categories


class ServeViewTestCase(TestCase):
    def setUp(self):
        self.view = PageMetadataReportView()
        self.tag1 = baker.make(Tag, name="tag1")
        self.tag2 = baker.make(Tag, name="tag2")
        self.site = Site.objects.get(is_default_site=True)
        self.root_page = self.site.root_page
        self.blog_page = BlogPage(title="Blogojevich", live=True)
        self.root_page.add_child(instance=self.blog_page)
        self.category_tuple = categories[0][1][0]
        self.category = CFGOVPageCategory(name=self.category_tuple[1])
        self.blog_page.categories.add(self.category)
        self.blog_page.tags.add(self.tag1, self.tag2)

    def test_process_categories(self):
        category_string = process_categories(self.blog_page.categories.all())
        self.assertIn(self.category.get_name_display(), category_string)
        self.assertEqual(
            self.category.get_name_display(), self.category_tuple[1]
        )

    def test_metadata_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.view.get_filename(), f"spreadsheet-export-{today}"
        )

    def test_get_queryset(self):
        self.assertEqual(self.view.get_queryset().count(), 2)
