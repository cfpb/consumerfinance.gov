from django.core.exceptions import ValidationError
from django.test import TestCase

from form_explainer.blocks import ImageMapCoordinates


class ImageMapCoordinatesTestCase(TestCase):
    def test_validation_fails_if_sum_of_top_and_height_exceeds_100(self):
        block = ImageMapCoordinates()
        value = block.to_python(
            {
                "left": 10,
                "top": 10,
                "width": 10,
                "height": 100,
            }
        )
        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_validation_fails_if_sum_of_left_and_width_exceeds_100(self):
        block = ImageMapCoordinates()
        value = block.to_python(
            {
                "left": 10,
                "top": 10,
                "width": 100,
                "height": 10,
            }
        )
        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_validates_if_coordinate_sums_less_than_or_equal_to_100(self):
        block = ImageMapCoordinates()
        value = block.to_python(
            {
                "left": 10,
                "top": 10,
                "width": 10,
                "height": 90,
            }
        )
        try:
            block.clean(value)
        except ValidationError:
            self.fail(
                "Validation should not fail for ImageMapCoordinates block "
                "when top/height and left/width sums are less than or equal "
                "to 100 and all values are between 0 and 100."
            )
