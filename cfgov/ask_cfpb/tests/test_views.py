from unittest import mock

from django.apps import apps
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.utils import timezone

from wagtail.core.models import Site
from wagtailsharing.models import SharingSite

from model_bakery import baker

from ask_cfpb.models import (
    ENGLISH_PARENT_SLUG,
    SPANISH_PARENT_SLUG,
    AnswerPage,
)
from ask_cfpb.views import annotate_links
from v1.util.migrations import get_or_create_page


now = timezone.now()


class AnswerPagePreviewTestCase(TestCase):
    def setUp(self):
        from ask_cfpb.models import Answer
        from v1.models import HomePage

        self.factory = RequestFactory()

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.english_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Ask CFPB",
            ENGLISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language="en",
            live=True,
        )
        self.spanish_parent_page = get_or_create_page(
            apps,
            "ask_cfpb",
            "AnswerLandingPage",
            "Obtener respuestas",
            SPANISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language="es",
            live=True,
        )
        self.test_answer = baker.make(Answer)
        self.test_answer2 = baker.make(Answer)
        self.english_answer_page = AnswerPage(
            answer_base=self.test_answer,
            language="en",
            slug="test-question1-en-{}".format(self.test_answer.pk),
            title="Test question1",
            answer_content="Test answer1.",
            question="Test question1.",
        )
        self.english_parent_page.add_child(instance=self.english_answer_page)
        self.english_answer_page.save_revision().publish()
        self.english_answer_page2 = AnswerPage(
            answer_base=self.test_answer2,
            language="en",
            slug="test-question2-en-{}".format(self.test_answer2.pk),
            title="Test question2",
            answer_content="Test answer2.",
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

    def test_page_redirected(self):
        page = self.english_answer_page
        page.get_latest_revision().publish()
        page.redirect_to_page = self.english_answer_page2
        page.save()
        page.save_revision().publish()
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, self.english_answer_page2.url)

    def test_redirect_view_with_no_recognized_facet(self):
        response = self.client.get("/askcfpb/search/?selected_facets=hoodoo")
        self.assertEqual(response.status_code, 404)


class AnswerViewTestCase(TestCase):
    def test_annotate_links(self):
        mock_answer = '<p>Answer with a <a href="http://fake.com">fake link.</a></p>'
        (annotated_answer, links) = annotate_links(mock_answer)
        self.assertEqual(
            annotated_answer,
            '<html><body><p>Answer with a <a href="http://fake.com">fake '
            "link.</a><sup>1</sup></p></body></html>",
        )
        self.assertEqual(links, [(1, str("http://fake.com"))])

    def test_annotate_links_no_href(self):
        mock_answer = "<p>Answer with a <a>fake link.</a></p>"
        (annotated_answer, links) = annotate_links(mock_answer)
        self.assertEqual(links, [])

    def test_annotate_links_no_site(self):
        site = Site.objects.get(is_default_site=True)
        site.is_default_site = False
        site.save()
        with self.assertRaises(RuntimeError) as context:
            annotate_links("answer")
        self.assertIn("no default wagtail site", str(context.exception))
