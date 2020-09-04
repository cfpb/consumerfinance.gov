from django.db import models
from django.utils.functional import cached_property

from wagtail.images.image_operations import (
    DoNothingOperation, MinMaxOperation, WidthHeightOperation
)
from wagtail.images.models import (
    AbstractImage, AbstractRendition, Filter, Image
)

from wagtail_placeholder_images.mixins import PlaceholderRenditionMixin


class CFGOVImage(PlaceholderRenditionMixin, AbstractImage):
    alt = models.CharField(max_length=100, blank=True)
    file_hash = models.CharField(max_length=40, blank=True, editable=False)
    admin_form_fields = Image.admin_form_fields + (
        'alt',
    )

    def get_rendition(self, rendition_filter):
        """Always return the source image file for GIF renditions.

        CFGOVImage overrides the default Wagtail renditions behavior to
        always embed the original uploaded image file for GIFs, instead of
        generating new versions on the fly.
        """
        if self.file.name.endswith('.gif'):
            return self.get_mock_rendition(rendition_filter)
        else:
            return super(CFGOVImage, self).get_rendition(rendition_filter)

    def get_mock_rendition(self, rendition_filter):
        """Create a mock rendition object that wraps the original image.

        Using the template tag {% image image 'original' %} will return an
        <img> tag linking to the original file (instead of a file copy, as
        is default Wagtail behavior).

        Template tags with Wagtail size-related filters (width, height, max,
        and min), e.g. {% image image 'max-165x165' %}, will generate an
        <img> tag with appropriate size parameters, following logic from
        wagtail.images.image_operations.
        """
        if isinstance(rendition_filter, str):
            rendition_filter = Filter(spec=rendition_filter)

        width = self.width
        height = self.height

        for operation in rendition_filter.operations:
            if isinstance(operation, DoNothingOperation):
                continue

            if not any([
                isinstance(operation, WidthHeightOperation),
                isinstance(operation, MinMaxOperation),
            ]):
                raise RuntimeError('non-size operations not supported on GIFs')

            width, height = self.apply_size_operation(operation, width, height)

        return CFGOVRendition(
            image=self,
            file=self.file,
            width=width,
            height=height
        )

    @staticmethod
    def apply_size_operation(operation, width, height):
        class MockResizableImage(object):
            def __init__(self, width, height):
                self.width = width
                self.height = height

            def get_size(self):
                return self.width, self.height

            def resize(self, size):
                width, height = size
                self.width = width
                self.height = height

        mock_image = MockResizableImage(width, height)
        operation.run(mock_image, image=None, env={})
        return mock_image.width, mock_image.height

    @property
    def default_alt_text(self):
        # Override Wagtail default of setting alt text to the image title.
        return self.alt

    # If the image is both large and its height-to-width ratio is approximately
    # 1/2 we instruct the template to render large Twitter cards
    # See https://dev.twitter.com/cards/types/summary-large-image
    @property
    def should_display_summary_large_image(self):
        image_ratio = float(self.height) / self.width
        return self.width >= 1000 and 0.4 <= image_ratio <= 0.6


class CFGOVRendition(AbstractRendition):
    image = models.ForeignKey(
        CFGOVImage,
        on_delete=models.CASCADE,
        related_name='renditions')

    @property
    def alt(self):
        return self.image.alt

    @cached_property
    def orientation(self):
        orientation = 'square'
        if self.is_portrait:
            orientation = 'portrait'
        elif self.is_landscape:
            orientation = 'landscape'

        return orientation

    @cached_property
    def is_square(self):
        return self.height == self.width

    @cached_property
    def is_portrait(self):
        return self.height > self.width

    @cached_property
    def is_landscape(self):
        return self.height < self.width

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
