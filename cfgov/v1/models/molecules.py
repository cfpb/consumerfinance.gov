import datetime

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from .base import CFGOVPage

def isRequired(field_name):
    return [str(field_name) + ' is required.']

class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    content = blocks.RichTextBlock(blank=True)
    links = blocks.ListBlock(blocks.StructBlock([
        ('text', blocks.CharBlock(required=False)),
        ('url', blocks.URLBlock(required=False)),
    ], icon='user', required=False)
    )

    class Meta:
        icon = 'link'
        template = 'v1/demo/molecules/half_width_link_blob.html'


class ImageText5050(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, required=True)
    description = blocks.RichTextBlock(blank=True)
    image = ImageChooserBlock(required=False)
    image_path = blocks.CharBlock(required=False)
    image_alt = blocks.CharBlock(required=False)
    is_widescreen = blocks.BooleanBlock(required=False)
    is_button = blocks.BooleanBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)

    def clean(self, data):
        ordered_tuples = data.items()
        error_dict = {}
        if not ordered_tuples[0][1]:
            error_dict['title'] = isRequired('Title')

        if not ordered_tuples[2][1] and not ordered_tuples[3][1] and not ordered_tuples[4][1]:
            img_err = ['Please upload or enter an image path']
            error_dict.update({'image': img_err, 'image_path': img_err, 'image_alt': isRequired('Image alt')})

        if ordered_tuples[2][1] and not ordered_tuples[3][1]:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'image': img_err,
                'image_path': img_err})

        if ordered_tuples[3][1] and not ordered_tuples[4][1]:
            error_dict.update({'image_alt': isRequired('Image Alt')})

        raise ValidationError("ImageText5050 validation errors", params=error_dict)

    class Meta:
        icon = 'image'
        template = 'v1/demo/molecules/image_text_5050.html'


class TextIntroduction(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    intro = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(max_length=100, required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'title'
        template = 'v1/demo/molecules/text_introduction.html'
