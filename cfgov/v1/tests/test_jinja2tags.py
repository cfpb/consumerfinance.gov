from django.test import TestCase
from model_mommy import mommy

from v1.atomic_elements.atoms import ImageBasic
from v1.jinja2tags import image_alt_value
from v1.models import CFGOVImage


class TestImageAltValue(TestCase):
    def test_no_image(self):
        block = ImageBasic()
        value = block.to_python({})
        self.assertEqual(image_alt_value(value), '')

    def test_no_alt_text_set(self):
        image_no_alt_text = mommy.make(CFGOVImage, alt='')
        block = ImageBasic()
        value = block.to_python({'upload': image_no_alt_text.pk, 'alt': ''})
        self.assertEqual(image_alt_value(value), '')

    def test_alt_text_on_upload(self):
        image_with_alt_text = mommy.make(CFGOVImage, alt='Alt text on upload')
        block = ImageBasic()
        value = block.to_python({'upload': image_with_alt_text.pk, 'alt': ''})
        self.assertEqual(image_alt_value(value), 'Alt text on upload')

    def test_alt_text_on_block(self):
        image_no_alt_text = mommy.make(CFGOVImage, alt='')
        block = ImageBasic()
        value = block.to_python({'upload': image_no_alt_text.pk,
                                 'alt': 'Alt text on block'})
        self.assertEqual(image_alt_value(value), 'Alt text on block')

    def test_alt_text_on_both(self):
        image_with_alt_text = mommy.make(CFGOVImage, alt='Alt text on upload')
        block = ImageBasic()
        value = block.to_python({'upload': image_with_alt_text.pk,
                                 'alt': 'Alt text on block'})
        self.assertEqual(image_alt_value(value), 'Alt text on block')
