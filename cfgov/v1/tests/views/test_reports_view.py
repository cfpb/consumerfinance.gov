import json
from datetime import date
from unittest import mock

from django.test import TestCase

from wagtail.core.models import Site
from wagtail.documents.models import Document

from model_bakery import baker
from taggit.models import Tag

from v1.models import BlogPage, CFGOVPage, CFGOVPageCategory
from v1.models.snippets import EmailSignUp
from v1.util.ref import categories
from v1.views.reports import (
    DocumentsReportView,
    EmailSignupReportView,
    PageMetadataReportView,
    construct_absolute_url,
    process_categories,
    process_tags,
)


class ServeViewTestCase(TestCase):
    def setUp(self):
        self.page_metadata_report_view = PageMetadataReportView()
        self.documents_report_view = DocumentsReportView()
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

    def test_metadata_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.page_metadata_report_view.get_filename(),
            f"wagtail-report_pages_{today}",
        )

    def test_metadata_report_get_queryset(self):
        self.assertEqual(
            self.page_metadata_report_view.get_queryset().count(), 2
        )

    def test_documents_report_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.documents_report_view.get_filename(),
            f"wagtail-report_documents_{today}",
        )

    def test_documents_report_get_queryset(self):
        self.assertEqual(self.documents_report_view.get_queryset().count(), 1)


class EmailSignupReportViewTestCase(TestCase):
    def setUp(self):
        self.email_signup_report_view = EmailSignupReportView()

        self.email_signup1 = EmailSignUp(
            topic="Test signup 1",
            code="TEST_CODE_1",
        )
        self.email_signup2 = EmailSignUp(
            topic="Test signup 2",
            code="TEST_CODE_2",
        )

        self.site = Site.objects.get(is_default_site=True)
        self.root_page = self.site.root_page

        self.regular_page = CFGOVPage(
            title="Random page",
            live=True,
            sidefoot=json.dumps(
                [
                    {
                        "type": "email_signup",
                        "value": self.email_signup1.pk,
                    }
                ]
            ),
        )
        self.root_page.add_child(instance=self.regular_page)

        self.blog_page = BlogPage(
            title="Blogojevich",
            live=True,
            content=json.dumps(
                [
                    {
                        "type": "email_signup",
                        "value": self.email_signup2.pk,
                    }
                ]
            ),
        )
        self.root_page.add_child(instance=self.blog_page)

    def test_get_filename(self):
        today = date.today()
        self.assertEqual(
            self.email_signup_report_view.get_filename(),
            f"wagtail-report_pages_with_email_signups_{today}",
        )

    def test_get_models_with_block(self):
        models_and_fields = list(
            self.email_signup_report_view.get_models_with_block(
                "email_signups"
            )
        )

        # Each model's field containing email_signups should be in this list
        self.assertIn((CFGOVPage, "sidefoot"), models_and_fields)
        self.assertIn((BlogPage, "content"), models_and_fields)

        # A super class's fields containing email_signups should not
        self.assertNotIn((BlogPage, "sidefoot"), models_and_fields)

    def test_get_queryset(self):
        # To keep this test simple, we patch the get_models_with_block method
        # on the report to
        with mock.patch.object(
            self.email_signup_report_view, "get_models_with_block"
        ) as mock_get_models_with_block:
            mock_get_models_with_block.return_value = [
                (CFGOVPage, "sidefoot"),
                (BlogPage, "content"),
            ]

            # The ORM complexity in this method should only result in 2 queries.
            with self.assertNumQueries(2):
                # One query should be evaluated within the get_queryset method.
                page_qs = self.email_signup_report_view.get_queryset()

                # The second query should be when we evaluate the returned
                # queryset.
                pages = list(page_qs)

        # We should get back our two test pages
        self.assertEqual(len(pages), 2)

        # They should have their respective email signup snippet pks as
        # email_signup_value
        self.assertEqual(pages[0].email_signup_value, self.email_signup1.pk)
        self.assertEqual(pages[1].email_signup_value, self.email_signup2.pk)
