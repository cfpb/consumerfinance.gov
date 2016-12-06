from django.test import TestCase
from mock import Mock
from wagtail.wagtailimages.models import Filter

from v1.models.images import CFGOVImage, CFGOVRendition


class CFGOVImageTest(TestCase):
    def test_no_renditions_by_default(self):
        self.assertFalse(CFGOVRendition.objects.exists())

    def test_image_original_rendition_image(self):
        image = CFGOVImage(file=Mock(), width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(rendition.image, image)

    def test_image_original_rendition_file(self):
        image = CFGOVImage(file=Mock(), width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(rendition.file, image.file)

    def test_image_original_rendition_size(self):
        image = CFGOVImage(file=Mock(), width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(rendition.width, image.width)
        self.assertEqual(rendition.height, image.height)

    def test_image_original_filter_class(self):
        image = CFGOVImage(file=Mock(), width=100, height=100)
        rendition_filter = Filter(spec='original')
        rendition = image.get_rendition(rendition_filter)
        self.assertEqual(rendition.file, image.file)

    def test_image_original_rendition_img_tag(self):
        mock_image = Mock(url='https://url')
        image = CFGOVImage(file=mock_image, width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(
            rendition.img_tag(),
            '<img alt="" height="100" src="https://url" width="100">'
        )

    def test_max_size_rendition(self):
        image = CFGOVImage(file=Mock(), width=100, height=100)
        rendition = image.get_rendition('max-165x165')
        self.assertEqual(rendition.width, 165)
        self.assertEqual(rendition.height, 165)

    def test_max_size_rendition_img_tag(self):
        mock_image = Mock(url='https://url')
        image = CFGOVImage(file=mock_image, width=100, height=100)
        rendition = image.get_rendition('max-165x165')
        self.assertEqual(
            rendition.img_tag(),
            '<img alt="" height="165" src="https://url" width="165">'
        )
