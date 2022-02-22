from datetime import date

from django.test import TestCase

from wagtail.core.models import Site
from wagtail.documents.models import Document

from model_bakery import baker
from taggit.models import Tag

from v1.models import BlogPage, CFGOVPageCategory
from v1.util.ref import categories
from v1.views.reports import (
    DocumentsReportView, PageMetadataReportView, construct_absolute_url,
    process_categories, process_tags
)


class ServeViewTestCase(TestCase):
    def setUp(self):
        self.page_metadata_report_view = PageMetadataReportView()
        self.documents_report_view = DocumentsReportView()
        self.tag1 = baker.make(Tag, name="tag1")
        self.tag2 = baker.make(Tag, name="tag2")
        self.site = Site.objects.get(is_default_site=True)
        self.root_page = self.site.root_page
        self.blog_page = BlogPage(title='Blogojevich', live=True)
        self.root_page.add_child(instance=self.blog_page)
        self.category_tuple = categories[0][1][0]
        self.category = CFGOVPageCategory(name=self.category_tuple[1])
        self.blog_page.categories.add(self.category)
        self.blog_page.tags.add(self.tag1, self.tag2)
        self.document = Document(title="Test document 1")
        self.document.save()
        self.document.tags.add(self.tag1, self.tag2)

    def test_construct_absolute_url(self):
        self.assertEqual(
            construct_absolute_url(self.blog_page.url),
            "https://www.consumerfinance.gov" + self.blog_page.url)

    def test_process_categories(self):
        category_string = process_categories(self.blog_page.categories.all())
        self.assertIn(
            self.category.get_name_display(), category_string)
        self.assertEqual(
            self.category.get_name_display(), self.category_tuple[1])

    def test_process_tags(self):
        tag_name_queryset = self.document.tags.all().values_list(
            'name', flat=True)
        tag_string = process_tags(tag_name_queryset)
        self.assertEqual(
            tag_string,
            'tag1, tag2'
        )

    def test_metadata_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.page_metadata_report_view.get_filename(),
            f"spreadsheet-export-{today}")

    def test_metadata_report_get_queryset(self):
        self.assertEqual(
            self.page_metadata_report_view.get_queryset().count(),
            2)

    def test_documents_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.documents_report_view.get_filename(),
            f"all-cfgov-documents-{today}")

    def test_documents_report_get_queryset(self):
        self.assertEqual(
            self.documents_report_view.get_queryset().count(),
            1)
