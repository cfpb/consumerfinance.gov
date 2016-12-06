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
