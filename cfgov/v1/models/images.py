from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.six import string_types
from wagtail.wagtailimages.image_operations import (DoNothingOperation,
                                                    MinMaxOperation,
                                                    WidthHeightOperation)
from wagtail.wagtailimages.models import (AbstractImage, AbstractRendition,
                                          Filter, Image)


class CFGOVImage(AbstractImage):
    alt = models.CharField(max_length=100, blank=True)

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
        wagtail.wagtailimages.image_operations.
        """
        if isinstance(rendition_filter, string_types):
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


class CFGOVRendition(AbstractRendition):
    image = models.ForeignKey(CFGOVImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CFGOVImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CFGOVRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
