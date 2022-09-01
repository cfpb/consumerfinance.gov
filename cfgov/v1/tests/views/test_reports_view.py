import json
from datetime import date

from django.test import TestCase
from django.utils import timezone

from wagtail.core.models import Site
from wagtail.documents.models import Document

from model_bakery import baker
from taggit.models import Tag

from v1.models import (
    BlogPage,
    CFGOVPageCategory,
    EnforcementActionPage,
    EnforcementActionProduct,
    EnforcementActionStatus,
)
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.ref import categories
from v1.views.reports import (
    AskReportView,
    DocumentsReportView,
    EnforcementActionsReportView,
    PageMetadataReportView,
    construct_absolute_url,
    process_categories,
    process_enforcement_action_page_content,
    process_related_items,
    process_tags,
    strip_html,
)


class ServeViewTestCase(TestCase):
    def setUp(self):
        self.page_metadata_report_view = PageMetadataReportView()
        self.documents_report_view = DocumentsReportView()
        self.ask_report_view = AskReportView()
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
        self.document = Document(title="Test document 1")
        self.document.save()
        self.document.tags.add(self.tag1, self.tag2)

        self.enforcement = EnforcementActionPage(
            title="Great Test Page",
            preview_description="This is a great test page.",
            initial_filing_date=timezone.now(),
        )
        self.html_content = "<p>Blog Text</p> <a href='www.test.com'>test</a>"
        self.content = json.dumps(
            [
                {
                    "type": "full_width_text",
                    "value": [
                        {
                            "type": "content",
                            "value": self.html_content,
                        },
                    ],
                },
            ]
        )

        status = EnforcementActionStatus(status="expired-terminated-dismissed")
        self.enforcement.statuses.add(status)
        self.enforcement.content = self.content
        product = EnforcementActionProduct(product="Fair Lending")
        self.enforcement.products.add(product)
        save_new_page(self.enforcement)

        self.enforcement_actions_report_view = EnforcementActionsReportView()

    def test_enforcement_report_get_queryset(self):
        self.assertEqual(
            self.enforcement_actions_report_view.get_queryset().count(), 1
        )

    def test_process_enforcement_content(self):
        self.assertTrue(
            process_enforcement_action_page_content(
                self.enforcement.content
            ).__contains__("Blog Text")
        )

    def test_enforcements_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.enforcement_actions_report_view.get_filename(),
            f"enforcement-actions-report-{today}",
        )

    def test_construct_absolute_url(self):
        self.assertEqual(
            construct_absolute_url(self.blog_page.url),
            "https://www.consumerfinance.gov" + self.blog_page.url,
        )

    def test_process_categories(self):
        category_string = process_categories(self.blog_page.categories.all())
        self.assertIn(self.category.get_name_display(), category_string)
        self.assertEqual(
            self.category.get_name_display(), self.category_tuple[1]
        )

    def test_process_tags(self):
        tag_name_queryset = self.document.tags.values_list("name", flat=True)
        tag_string = process_tags(tag_name_queryset)
        self.assertEqual(tag_string, "tag1, tag2")

    def test_process_related_items(self):
        all_pages = self.root_page.get_children()
        page_titles_string = process_related_items(all_pages, "title")
        self.assertEqual(page_titles_string, "Blogojevich | Great Test Page")

    def test_strip_html(self):
        stripped_content = strip_html(self.html_content)
        self.assertEqual(stripped_content, "Blog Text test")

    def test_metadata_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.page_metadata_report_view.get_filename(),
            f"wagtail-report_pages_{today}",
        )

    def test_metadata_report_get_queryset(self):
        self.assertEqual(
            self.page_metadata_report_view.get_queryset().count(), 3
        )

    def test_documents_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.documents_report_view.get_filename(),
            f"wagtail-report_documents_{today}",
        )

    def test_documents_report_get_queryset(self):
        self.assertEqual(self.documents_report_view.get_queryset().count(), 1)

    def test_ask_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.ask_report_view.get_filename(),
            f"wagtail-report_ask-cfpb_{today}",
        )
