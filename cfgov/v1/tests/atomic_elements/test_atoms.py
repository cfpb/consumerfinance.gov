from django.test import TestCase

from wagtail.images.tests.utils import get_test_image_file

from v1.atomic_elements.atoms import ImageBasic
from v1.models import CFGOVImage


def make_image(alt_text):
    return CFGOVImage.objects.create(
        title='test',
        file=get_test_image_file(),
        alt=alt_text
    )


class ImageBasicTests(TestCase):
    def test_value_no_upload_undefined_url_and_alt_text(self):
        block = ImageBasic()
        value = block.to_python({})
        self.assertIsNone(value.url)
        self.assertIsNone(value.alt_text)

    def test_value_no_alt_returns_empty_string(self):
        image = make_image(alt_text='')

        block = ImageBasic()
        value = block.to_python({'upload': image.pk})

        self.assertRegex(value.url, r'^.*/images/test.*\.original\.png$')
        self.assertEqual(value.alt_text, '')

    def test_value_image_alt(self):
        image = make_image(alt_text='Image alt text')

        block = ImageBasic()
        value = block.to_python({'upload': image.pk})

        self.assertRegex(value.url, r'^.*/images/test.*\.original\.png$')
        self.assertEqual(value.alt_text, 'Image alt text')

    def test_value_block_alt(self):
        image = make_image(alt_text='Image alt text')

        block = ImageBasic()
        value = block.to_python({
            'upload': image.pk,
            'alt': 'ImageBasic alt text',
        })

        self.assertRegex(value.url, r'^.*/images/test.*\.original\.png$')
        self.assertEqual(value.alt_text, 'ImageBasic alt text')
