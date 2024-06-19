import json
from unittest import mock

from django.http import Http404
from django.test import RequestFactory, TestCase
from django.utils import timezone

from wagtail.models import Site

from model_bakery import baker
from wagtailsharing.models import SharingSite

from ask_cfpb.models import (
    ENGLISH_PARENT_SLUG,
    SPANISH_PARENT_SLUG,
    AnswerLandingPage,
    AnswerPage,
)


now = timezone.now()


class AnswerPagePreviewTestCase(TestCase):
    def setUp(self):
        from ask_cfpb.models import Answer
        from v1.models import HomePage

        self.factory = RequestFactory()

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")

        self.english_parent_page = AnswerLandingPage(
            title="Ask CFPB",
            slug=ENGLISH_PARENT_SLUG,
            language="en",
            live=True,
        )
        self.ROOT_PAGE.add_child(instance=self.english_parent_page)

        self.spanish_parent_page = AnswerLandingPage(
            title="Obtener respuestas",
            slug=SPANISH_PARENT_SLUG,
            language="es",
            live=True,
        )
        self.ROOT_PAGE.add_child(instance=self.spanish_parent_page)

        self.test_answer = baker.make(Answer)
        self.test_answer2 = baker.make(Answer)
        self.english_answer_page = AnswerPage(
            answer_base=self.test_answer,
            language="en",
            slug=f"test-question1-en-{self.test_answer.pk}",
            title="Test question1",
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Test answer1",
                        },
                    }
                ]
            ),
            question="Test question1.",
        )
        self.english_parent_page.add_child(instance=self.english_answer_page)
        self.english_answer_page.save_revision().publish()
        self.english_answer_page2 = AnswerPage(
            answer_base=self.test_answer2,
            language="en",
            slug=f"test-question2-en-{self.test_answer2.pk}",
            title="Test question2",
            answer_content=json.dumps(
                [
                    {
                        "type": "text",
                        "value": {
                            "anchor_tag": "",
                            "content": "Test answer2",
                        },
                    }
                ]
            ),
            question="Test question2.",
        )
        self.english_parent_page.add_child(instance=self.english_answer_page2)
        self.english_answer_page2.save_revision().publish()
        self.site = baker.make(
            Site,
            root_page=self.ROOT_PAGE,
            hostname="localhost",
            port=8000,
            is_default_site=True,
        )
        self.sharing_site = baker.make(
            SharingSite,
            site=self.site,
            hostname="preview.localhost",
            port=8000,
        )

    @mock.patch("ask_cfpb.views.ServeView.serve")
    def test_live_plus_draft_with_sharing(self, mock_serve):
        from ask_cfpb.views import view_answer

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        page = self.test_answer.english_page
        page.title += " more title"
        page.save_revision(user=None)
        slug = page.slug
        pk = page.answer_base.pk
        view_answer(test_request, slug, "en", pk)
        self.assertEqual(mock_serve.call_count, 1)

    @mock.patch("ask_cfpb.views.ServeView.serve")
    def test_live_plus_draft_no_sharing(self, mock_serve):
        from ask_cfpb.views import view_answer

        test_request = self.factory.get("/")
        page = self.test_answer.english_page
        page.title += " more title"
        page.save_revision(user=None)
        slug = page.slug
        pk = page.answer_base.pk
        response = view_answer(test_request, slug, "en", pk)
        self.assertEqual(mock_serve.call_count, 0)
        self.assertEqual(response.status_code, 200)

    def test_answer_page_not_live(self):
        from ask_cfpb.views import view_answer

        page = self.test_answer.english_page
        page.unpublish()
        test_request = self.factory.get("/")
        with self.assertRaises(Http404):
            view_answer(test_request, page.slug, "en", page.answer_base.pk)

    @mock.patch("ask_cfpb.views.ServeView.serve")
    def test_answer_page_not_live_on_sharing_site(self, mock_serve):
        from ask_cfpb.views import view_answer

        page = self.test_answer.english_page
        page.unpublish()
        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        view_answer(test_request, "test-question1", "en", self.test_answer.pk)
        self.assertEqual(mock_serve.call_count, 1)

    def test_redirect_view_with_no_recognized_facet(self):
        response = self.client.get("/askcfpb/search/?selected_facets=hoodoo")
        self.assertEqual(response.status_code, 404)
