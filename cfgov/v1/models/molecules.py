import datetime

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from .base import CFGOVPage


class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=False)
    content = blocks.RichTextBlock(blank=True)
    links = blocks.ListBlock(blocks.StructBlock([
        ('text', blocks.CharBlock(required=False)),
        ('url', blocks.URLBlock(required=False)),
    ], icon='user', required=False)
    )

    class Meta:
        icon = 'link'
        template = '_includes/molecules/half_width_link_blob.html'


class ImageText5050(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, required=False)
    description = blocks.RichTextBlock(blank=True)
    image = ImageChooserBlock(required=False)
    image_path = blocks.CharBlock(blank=True)
    image_alt = blocks.CharBlock(blank=True)
    is_widescreen = blocks.BooleanBlock(required=False)
    is_button = blocks.BooleanBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/image_text_5050.html',


class TextIntroduction(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=False)
    intro = blocks.CharBlock(max_length=100, required=False)
    body = blocks.RichTextBlock(blank=True)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'title'
        template = '_includes/molecules/text_introduction.html'
