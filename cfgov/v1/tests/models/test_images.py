from unittest.mock import Mock, patch

from django.db import IntegrityError
from django.test import TestCase

from wagtail.images.models import Filter
from wagtail.images.tests.utils import get_test_image_file

from v1.models.images import CFGOVImage, CFGOVRendition


class CFGOVImageTest(TestCase):
    def setUp(self):
        def mock_with_name(name):
            mock = Mock()
            mock.configure_mock(name=name, url='https://url')
            return mock

        self.mock_gif = mock_with_name('test.gif')
        self.mock_png = mock_with_name('test.png')

    def test_no_renditions_by_default(self):
        self.assertFalse(CFGOVRendition.objects.exists())

    def test_original_rendition_calls_super_for_png(self):
        image = CFGOVImage(file=self.mock_png, width=100, height=100)
        with patch('v1.models.images.AbstractImage.get_rendition') as p:
            image.get_rendition('original')
            p.assert_called_once_with('original')

    def test_original_rendition_makes_mock_rendition_for_gif(self):
        image = CFGOVImage(file=self.mock_gif, width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(rendition.image, image)

    def test_non_resize_rendition_calls_super_for_png(self):
        with patch('v1.models.images.AbstractImage.get_rendition') as p:
            image = CFGOVImage(file=self.mock_png, width=100, height=100)
            image.get_rendition('fill-200x200')
            p.assert_called_once_with('fill-200x200')

    def test_non_resize_rendition_raises_for_gif(self):
        image = CFGOVImage(file=self.mock_gif, width=100, height=100)
        with self.assertRaises(RuntimeError):
            image.get_rendition('fill-200x200')

    def test_image_original_rendition_size(self):
        image = CFGOVImage(file=self.mock_gif, width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(rendition.width, image.width)
        self.assertEqual(rendition.height, image.height)

    def test_image_original_filter_class(self):
        image = CFGOVImage(file=self.mock_gif, width=100, height=100)
        rendition_filter = Filter(spec='original')
        rendition = image.get_rendition(rendition_filter)
        self.assertEqual(rendition.file, image.file)

    def test_image_original_rendition_img_tag(self):
        image = CFGOVImage(file=self.mock_gif, width=100, height=100)
        rendition = image.get_rendition('original')
        self.assertEqual(
            rendition.img_tag(),
            '<img alt="" height="100" src="https://url" width="100">'
        )

    def test_max_size_rendition(self):
        image = CFGOVImage(file=self.mock_gif, width=100, height=100)
        rendition = image.get_rendition('max-165x165')
        self.assertEqual(rendition.width, 100)
        self.assertEqual(rendition.height, 100)

    def test_max_size_rendition_img_tag(self):
        mock_image = Mock(url='https://url')
        image = CFGOVImage(file=mock_image, width=100, height=100)
        rendition = image.get_rendition('max-165x165')
        self.assertEqual(
            rendition.img_tag(),
            '<img alt="" height="100" src="https://url" width="100">'
        )

    def test_width_rendition_size(self):
        image = CFGOVImage(file=self.mock_gif, width=500, height=300)
        rendition = image.get_rendition('width-250')
        self.assertEqual(
            (rendition.width, rendition.height),
            (250, 150)
        )

    def test_width_rendition_img_tag(self):
        image = CFGOVImage(file=self.mock_gif, width=500, height=300)
        rendition = image.get_rendition('width-250')
        self.assertEqual(
            rendition.img_tag(),
            '<img alt="" height="150" src="https://url" width="250">'
        )

    def test_twitter_card_large(self):
        """Twitter card property should be true if meta image is large"""
        image = CFGOVImage(width=1200, height=600)
        self.assertTrue(image.should_display_summary_large_image)

    def test_twitter_card_small(self):
        """Twitter card property should be false if meta image is small"""
        image = CFGOVImage(width=100, height=50)
        self.assertFalse(image.should_display_summary_large_image)

    def test_twitter_card_large_bad_ratio(self):
        """Twitter card property should be false if meta image ratio < 50%"""
        image = CFGOVImage(width=1200, height=100)
        self.assertFalse(image.should_display_summary_large_image)


class CFGOVRenditionTest(TestCase):
    def test_uniqueness_constraint(self):
        image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )

        filt = Filter(spec='original')

        def create_rendition(image, filt):
            return CFGOVRendition.objects.create(
                filter_spec=filt.spec,
                image=image,
                file=image.file,
                width=100,
                height=100,
                focal_point_key=filt.get_cache_key(image)
            )

        create_rendition(image=image, filt=filt)
        with self.assertRaises(IntegrityError):
            create_rendition(image=image, filt=filt)
