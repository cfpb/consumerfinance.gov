from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.six import string_types
from wagtail.wagtailimages.image_operations import MinMaxOperation
from wagtail.wagtailimages.models import (
    AbstractImage, AbstractRendition, Filter, Image
)


class CFGOVImage(AbstractImage):
    alt = models.CharField(max_length=100, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'alt',
    )

    def get_rendition(self, rendition_filter):
        """Always return the source image file when renditions are requested.

        CFGOVImage overrides the default Wagtail renditions behavior to
        always embed the original uploaded image file, instead of generating
        new versions on the fly.

        By default using the template tag {% image image 'original' %} will
        return an <img> tag linking to the original file (instead of a file
        copy, as is default Wagtail behavior.)

        Using a template tag with a maximum image size like
        {% image image 'max-165x165' %} will generate an <img> tag with
        the specified size parameters, i.e. <img width="165" height="165">.
        """
        if isinstance(rendition_filter, string_types):
            rendition_filter = Filter(spec=rendition_filter)

        width = self.width
        height = self.height

        for operation in rendition_filter.operations:
            if isinstance(operation, MinMaxOperation):
                if 'max' == operation.method:
                    width = operation.width
                    height = operation.height

        return CFGOVRendition(
            image=self,
            file=self.file,
            width=width,
            height=height
        )


class CFGOVRendition(AbstractRendition):
    image = models.ForeignKey(CFGOVImage, related_name='renditions')


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CFGOVImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CFGOVRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
