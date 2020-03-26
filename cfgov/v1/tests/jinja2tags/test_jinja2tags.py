from datetime import date

from django.template import engines
from django.test import RequestFactory, TestCase, override_settings

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
