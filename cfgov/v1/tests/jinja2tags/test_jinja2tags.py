import re
from datetime import date

from django.http import HttpRequest
from django.template import engines
from django.test import (
    RequestFactory, SimpleTestCase, TestCase, override_settings
)

from model_bakery import baker

from v1.atomic_elements.atoms import ImageBasic
from v1.jinja2tags import complaint_issue_banner, email_popup, image_alt_value
from v1.models import CFGOVImage, CFGOVRendition


class TestImageAltValue(TestCase):
    def test_no_rendition_or_block_passed(self):
        self.assertEqual(image_alt_value(None), '')

    def test_rendition_no_alt_text_set(self):
        rendition = CFGOVRendition(image=CFGOVImage())
        self.assertEqual(image_alt_value(rendition), '')

    def test_rendition_with_alt_text(self):
        rendition = CFGOVRendition(image=CFGOVImage(alt='Alt text'))
        self.assertEqual(image_alt_value(rendition), 'Alt text')

    def test_block_no_image_in_block(self):
        block = ImageBasic()
        value = block.to_python({})
        self.assertEqual(image_alt_value(value), '')

    def test_block_no_alt_text_set(self):
        image_no_alt_text = baker.make(CFGOVImage, alt='')
        block = ImageBasic()
        value = block.to_python({'upload': image_no_alt_text.pk, 'alt': ''})
        self.assertEqual(image_alt_value(value), '')

    def test_block_alt_text_on_upload(self):
        image_with_alt_text = baker.make(CFGOVImage, alt='Alt text on upload')
        block = ImageBasic()
        value = block.to_python({'upload': image_with_alt_text.pk, 'alt': ''})
        self.assertEqual(image_alt_value(value), 'Alt text on upload')

    def test_block_alt_text_on_block(self):
        image_no_alt_text = baker.make(CFGOVImage, alt='')
        block = ImageBasic()
        value = block.to_python({'upload': image_no_alt_text.pk,
                                 'alt': 'Alt text on block'})
        self.assertEqual(image_alt_value(value), 'Alt text on block')

    def test_block_alt_text_on_both(self):
        image_with_alt_text = baker.make(CFGOVImage, alt='Alt text on upload')
        block = ImageBasic()
        value = block.to_python({'upload': image_with_alt_text.pk,
                                 'alt': 'Alt text on block'})
        self.assertEqual(image_alt_value(value), 'Alt text on block')


class TestEmailPopup(TestCase):
    def test_email_popup_defined_and_returns_empty_for_no_popup(self):
        request = RequestFactory().get('/page/without/a/popup')
        self.assertEqual(email_popup(request), '')


class TestIsFilterSelected(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.jinja_engine = engines['wagtail-env']

    def _render_template_with_request(self, request):
        s = '{{ is_filter_selected("foo", "bar") }}'
        template = self.jinja_engine.from_string(s)
        return template.render({'request': request})

    def test_query_parameter_undefined_not_selected(self):
        request = self.factory.get('/')
        self.assertEqual(self._render_template_with_request(request), 'False')

    def test_query_parameter_defined_with_expected_value(self):
        request = self.factory.get('/?foo=bar')
        self.assertEqual(self._render_template_with_request(request), 'True')

    def test_query_parameter_defined_with_unexpected_value(self):
        request = self.factory.get('/?foo=baz')
        self.assertEqual(self._render_template_with_request(request), 'False')

    def test_query_parameter_defined_multiple_times(self):
        request = self.factory.get('/?foo=bar&foo=baz')
        self.assertEqual(self._render_template_with_request(request), 'True')

    def test_query_parameter_also_works_with_filter_prefix(self):
        request = self.factory.get('/?filter_foo=bar')
        self.assertEqual(self._render_template_with_request(request), 'True')

    def test_query_parameter_archived_selected(self):
        request = self.factory.get('/')
        s = '{{ is_filter_selected("archived", "include") }}'
        template = self.jinja_engine.from_string(s)
        self.assertEqual(template.render({'request': request}), 'True')


class TestUniqueIdInContext(TestCase):

    def setUp(self):
        self.engine = engines['wagtail-env']
        self.template = '{{ unique_id_in_context() }}'
        self.random_id_pattern = re.compile('[a-z0-9]{14}')

    def render(self, template, context=None):
        return self.engine.from_string(template).render(context=context)

    def assert_is_random_id(self, input):
        match = self.random_id_pattern.match(input)
        self.assertIsNotNone(match)

    def assert_is_not_random_id(self, input):
        match = self.random_id_pattern.match(input)
        self.assertIsNone(match)

    def test_no_context_returns_random_string(self):
        rendered = self.render(self.template)
        self.assert_is_random_id(rendered)

    def test_no_request_in_context_returns_random_string(self):
        rendered = self.render(self.template, {})
        self.assert_is_random_id(rendered)

    def test_render_with_request_in_context(self):
        rendered = self.render(self.template, {'request': HttpRequest()})
        self.assertEqual(rendered, '1')
        self.assert_is_not_random_id(rendered)

    def test_render_uses_request_to_make_multiple_unique_ids(self):
        request = HttpRequest()
        template = ' and '.join([self.template, self.template])
        self.assertEqual(
            self.render(template, {'request': request}),
            '1 and 2'
        )

    def test_multiple_renders_multiple_unique_ids(self):
        request = HttpRequest()
        rendered = [
            self.render(self.template, {'request': request})
            for _ in range(5)
        ]
        self.assertEqual(rendered, ['1', '2', '3', '4', '5'])

    def test_different_requests_allow_repeats(self):
        for i in range(5):
            self.assertEqual(
                self.render(self.template, {'request': HttpRequest()}),
                '1'
            )


class SearchGovAffiliateTests(SimpleTestCase):
    def render(self, context):
        engine = engines['wagtail-env']
        template = engine.from_string('{{ search_gov_affiliate() }}')
        return template.render(context=context)

    def test_default_cfpb(self):
        self.assertEqual(self.render({}), 'cfpb')

    def test_spanish(self):
        self.assertEqual(self.render({'language': 'es'}), 'cfpb_es')

    @override_settings(DEPLOY_ENVIRONMENT='beta')
    def test_beta(self):
        self.assertEqual(self.render({}), 'cfpb_beta')

    @override_settings(DEPLOY_ENVIRONMENT='beta')
    def test_beta_spanish(self):
        self.assertEqual(self.render({'language': 'es'}), 'cfpb_beta_es')
