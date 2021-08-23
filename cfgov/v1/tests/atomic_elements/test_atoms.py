from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from wagtail.images.tests.utils import get_test_image_file

from v1.atomic_elements.atoms import ImageBasic, URLOrRelativeURLBlock
from v1.models import CFGOVImage


class URLOrRelativeURLBlockTests(SimpleTestCase):
    def setUp(self):
        self.block = URLOrRelativeURLBlock()

    def check_clean(self, url):
        self.assertEqual(self.block.clean(url), url)

    def test_clean_absolute_url(self):
        self.check_clean('https://www.consumerfinance.gov/foo/bar/')

    def test_clean_relative_url(self):
        self.check_clean('/foo/bar/')

    def test_clean_invalid_url_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self.check_clean('url with spaces')


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
