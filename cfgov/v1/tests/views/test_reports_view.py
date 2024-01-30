import json
from datetime import date
from operator import itemgetter

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from wagtail.documents.models import Document
from wagtail.models import Site
from wagtail.test.utils import WagtailTestUtils

from model_bakery import baker
from taggit.models import Tag

from ask_cfpb.models import AnswerPage
from v1.models import (
    BlogPage,
    BrowsePage,
    CFGOVPageCategory,
    EnforcementActionPage,
    EnforcementActionProduct,
    EnforcementActionStatus,
)
from v1.tests.wagtail_pages.helpers import save_new_page
from v1.util.ref import categories
from v1.views.reports import (
    ActiveUsersReportView,
    AskReportView,
    CategoryIconReportView,
    DocumentsReportView,
    EnforcementActionsReportView,
    PageMetadataReportView,
    construct_absolute_url,
    join_values_with_pipe,
    process_categories,
    process_enforcement_action_page_content,
    process_related_item,
    process_tags,
    strip_html,
)


class ServeViewTestCase(TestCase):
    def setUp(self):
        # Shared items
        self.site = Site.objects.get(is_default_site=True)
        self.root_page = self.site.root_page
        self.category_tuple = categories[0][1][0]
        self.category = CFGOVPageCategory(name=self.category_tuple[1])
        self.html_content = (
            "<p>Test content</p> <a href='www.test.com'>test</a>"
        )
        self.full_width_text_content = json.dumps(
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
        self.tag1 = baker.make(Tag, name="tag1")
        self.tag2 = baker.make(Tag, name="tag2")

        # Page metadata report
        self.page_metadata_report_view = PageMetadataReportView()
        self.blog_page = BlogPage(title="Blogojevich", live=True)
        self.root_page.add_child(instance=self.blog_page)
        self.blog_page.categories.add(self.category)
        self.blog_page.tags.add(self.tag1, self.tag2)

        # Enforcement actions report
        self.enforcement_actions_report_view = EnforcementActionsReportView()
        self.enforcement = EnforcementActionPage(
            title="Great Test Page",
            initial_filing_date=timezone.now(),
        )
        status = EnforcementActionStatus(status="expired-terminated-dismissed")
        self.enforcement.statuses.add(status)
        self.enforcement.content = self.full_width_text_content
        product = EnforcementActionProduct(product="Fair Lending")
        self.enforcement.products.add(product)
        save_new_page(self.enforcement)

        # Documents report
        self.documents_report_view = DocumentsReportView()
        self.document = Document(title="Test document 1")
        self.document.save()
        self.document.tags.add(self.tag1, self.tag2)

        # Ask report
        self.ask_report_view = AskReportView()
        self.ask_page_with_content = AnswerPage(
            slug="ask-page-with-content",
            title="Ask Page with Content",
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "type": "content",
                            "content": self.html_content,
                        },
                    },
                ]
            ),
        )
        self.ask_page_with_schema = AnswerPage(
            slug="ask-page-with-schema",
            title="Ask Page with Schema",
            answer_content=json.dumps(
                [
                    {
                        "type": "how_to_schema",
                        "value": {
                            "type": "content",
                            "description": "<p>How-to description</p>",
                        },
                    },
                ]
            ),
        )
        self.ask_page_without_content = AnswerPage(
            slug="ask-page-no-content", title="Ask Page without Content"
        )
        self.root_page.add_child(instance=self.ask_page_with_content)
        self.root_page.add_child(instance=self.ask_page_with_schema)
        self.root_page.add_child(instance=self.ask_page_without_content)

    # Shared methods
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

    def test_process_related_item(self):
        related_page = self.blog_page
        related_page_id = process_related_item(related_page, "id")
        missing_page = None
        missing_page_id = process_related_item(missing_page, "id")
        self.assertTrue(len(related_page_id) > 0)
        self.assertEqual(missing_page_id, "")

    def test_join_values_with_pipe(self):
        all_pages = self.root_page.get_children()
        all_pages_count = len(all_pages)
        page_titles_string = join_values_with_pipe(all_pages, "title")
        pipe_count = page_titles_string.count("|")
        self.assertEqual(
            all_pages_count,
            pipe_count + 1,
        )

    def test_strip_html(self):
        stripped_content = strip_html(self.html_content)
        self.assertEqual(stripped_content, "Test content test")

    # Page metadata report
    def test_metadata_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.page_metadata_report_view.get_filename(),
            f"wagtail-report_pages_{today}",
        )

    def test_metadata_report_get_queryset(self):
        self.assertEqual(
            self.page_metadata_report_view.get_queryset().count(), 6
        )

    # Enforcement actions report
    def test_enforcements_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.enforcement_actions_report_view.get_filename(),
            f"enforcement-actions-report-{today}",
        )

    def test_enforcement_report_get_queryset(self):
        self.assertEqual(
            self.enforcement_actions_report_view.get_queryset().count(), 1
        )

    def test_process_enforcement_content(self):
        self.assertTrue(
            process_enforcement_action_page_content(
                self.enforcement.content
            ).__contains__("Test content")
        )

    # Documents report
    def test_documents_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.documents_report_view.get_filename(),
            f"wagtail-report_documents_{today}",
        )

    def test_documents_report_get_queryset(self):
        self.assertEqual(self.documents_report_view.get_queryset().count(), 1)

    # Ask report
    def test_ask_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.ask_report_view.get_filename(),
            f"wagtail-report_ask-cfpb_{today}",
        )

    def test_ask_report_get_queryset(self):
        self.assertEqual(self.ask_report_view.get_queryset().count(), 3)

    def test_process_answer_content(self):
        ask_page_content = AskReportView.process_answer_content(
            self.ask_page_with_content.answer_content
        )
        ask_page_schema_content = AskReportView.process_answer_content(
            self.ask_page_with_schema.answer_content
        )
        blank_ask_page_content = AskReportView.process_answer_content(
            self.ask_page_without_content.answer_content
        )
        self.assertEqual(ask_page_content, "Test content test")
        self.assertEqual(ask_page_schema_content, "How-to description")
        self.assertEqual(blank_ask_page_content, "")


class TestCategoryIconsReport(SimpleTestCase):
    def test_get_queryset(self):
        self.assertEqual(
            len(CategoryIconReportView().get_queryset()),
            sum(map(len, map(itemgetter(1), categories))),
        )


class TestTranslatedPagesReport(TestCase, WagtailTestUtils):
    def setUp(self):
        self.site_root = Site.objects.get(is_default_site=True).root_page
        self.url = reverse("translated_pages_report")

        self.login()

    def test_empty_report(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Translated Pages")
        self.assertContains(response, "No pages found.")

    def test_report_with_results_and_filtering(self):
        self.english_page = BrowsePage(title="en", slug="en", live=True)
        self.site_root.add_child(instance=self.english_page)
        self.spanish_page = BrowsePage(
            title="es",
            slug="es",
            language="es",
            live=True,
            english_page=self.english_page,
        )
        self.site_root.add_child(instance=self.spanish_page)

        response = self.client.get(self.url)
        self.assertContains(response, "Translated Pages")
        self.assertNotContains(response, "No pages found.")

        response = self.client.get(self.url + "?language=es")
        self.assertContains(response, "Translated Pages")
        self.assertNotContains(response, "No pages found.")

        response = self.client.get(self.url + "?language=ht")
        self.assertContains(response, "Translated Pages")
        self.assertContains(response, "No pages found.")


class TestActiveUsersReport(TestCase):
    def test_get_queryset(self):
        User = get_user_model()
        test_user = User(
            username="test", email="test@example.com", is_active=False
        )
        test_user.save()

        report_users = ActiveUsersReportView().get_queryset()
        self.assertGreater(len(User.objects.all()), len(report_users))
        self.assertNotIn(test_user, report_users)
