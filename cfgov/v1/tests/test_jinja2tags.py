from datetime import date

from django.test import TestCase

from model_mommy import mommy

from v1.atomic_elements.atoms import ImageBasic
from v1.jinja2tags import date_formatter, image_alt_value
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
        image_no_alt_text = mommy.make(CFGOVImage, alt='')
        block = ImageBasic()
        value = block.to_python({'upload': image_no_alt_text.pk, 'alt': ''})
        self.assertEqual(image_alt_value(value), '')

    def test_block_alt_text_on_upload(self):
        image_with_alt_text = mommy.make(CFGOVImage, alt='Alt text on upload')
        block = ImageBasic()
        value = block.to_python({'upload': image_with_alt_text.pk, 'alt': ''})
        self.assertEqual(image_alt_value(value), 'Alt text on upload')

    def test_block_alt_text_on_block(self):
        image_no_alt_text = mommy.make(CFGOVImage, alt='')
        block = ImageBasic()
        value = block.to_python({'upload': image_no_alt_text.pk,
                                 'alt': 'Alt text on block'})
        self.assertEqual(image_alt_value(value), 'Alt text on block')

    def test_block_alt_text_on_both(self):
        image_with_alt_text = mommy.make(CFGOVImage, alt='Alt text on upload')
        block = ImageBasic()
        value = block.to_python({'upload': image_with_alt_text.pk,
                                 'alt': 'Alt text on block'})
        self.assertEqual(image_alt_value(value), 'Alt text on block')


class TestDateFormatter(TestCase):
    def test_text_format_date(self):
        test_date = date(2018, 9, 5)
        output = date_formatter(test_date, text_format=True)
        self.assertIn('Sept. 5, 2018', output)

    def test_default_format_date(self):
        test_date = date(2018, 9, 5)
        output = date_formatter(test_date, text_format=False)
        self.assertIn('Sep 05, 2018', output)
