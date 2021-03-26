from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from wagtail.core.models import Page, Site

from ask_cfpb.models import Answer, AnswerLandingPage, AnswerPage
from ask_cfpb.wagtail_hooks import create_answer_id, editor_css


class TestAskHooks(TestCase):
    fixtures = ['ask_tests.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.default_site = Site.objects.get(is_default_site=True)
        self.site_root = Page.objects.get(slug='root')
        self.spanish_landing_page = AnswerLandingPage(
            title="Obtener respuestas",
            slug='obtener-respuestas',
            language='es')
        self.site_root.add_child(instance=self.spanish_landing_page)
        self.spanish_landing_page.save()
        self.spanish_landing_page.save_revision(user=self.user).publish()
        self.english_landing_page = AnswerLandingPage(
            title="Ask CFPB",
            slug='ask-cfpb',
            language='en')
        self.site_root.add_child(instance=self.english_landing_page)
        self.english_landing_page.save()
        self.english_landing_page.save_revision(user=self.user).publish()

    def test_js_functions(self):
        self.assertIn("css/question-tips.css", editor_css())

    def test_create_answer_id_english(self):
        """Test that English page creation generates an Ask ID and pages."""
        request = HttpRequest
        request.user = self.user
        test_page = AnswerPage(
            slug='test-page', title='Test page')
        self.english_landing_page.add_child(instance=test_page)
        test_page.save()
        create_answer_id(request, test_page)
        self.assertEqual(test_page.slug, 'test-page-en-{}'.format(
            Answer.objects.order_by('pk').last().pk))
        self.assertIsNotNone(test_page.answer_base)
        self.assertIsNotNone(test_page.answer_base.english_page)
        self.assertIsNotNone(test_page.answer_base.spanish_page)

    def test_create_answer_id_spanish(self):
        """Test that Spanish page creation generates an Ask ID and pages."""
        request = HttpRequest
        request.user = self.user
        test_page = AnswerPage(
            slug='spanish-page-1', title='Spanish page 1', language='es')
        self.spanish_landing_page.add_child(instance=test_page)
        test_page.save()
        create_answer_id(request, test_page)
        self.assertEqual(test_page.slug, 'spanish-page-1-es-{}'.format(
            Answer.objects.order_by('pk').last().pk))
        self.assertIsNotNone(test_page.answer_base)
        self.assertIsNotNone(test_page.answer_base.english_page)
        self.assertIsNotNone(test_page.answer_base.spanish_page)
