import datetime

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from .base import CFGOVPage


class Well(blocks.StructBlock):
    template_path = blocks.CharBlock(required=True)

    class Meta:
        icon = 'link'
        template = '_includes/organisms/well.html'
