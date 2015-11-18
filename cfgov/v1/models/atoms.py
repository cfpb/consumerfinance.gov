from django.core.exceptions import ValidationError

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


def isRequired(field_name):
    return [str(field_name) + ' is required.']


class Hyperlink(blocks.StructBlock):
    text = blocks.CharBlock(max_length=50)
    url = blocks.CharBlock(default='/')


class ImageBasic(blocks.StructBlock):
    upload = ImageChooserBlock(required=False)
    url = blocks.CharBlock(required=False)
    alt = blocks.CharBlock(required=False)

    def clean(self, data):
        error_dict = {}
        try:
            block_data = super(ImageBasic, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)
            block_data = data

        if not block_data['upload'] and not block_data['url'] and not block_data['alt']:
            img_err = ['Please upload or enter an image path']
            error_dict.update({'upload': img_err, 'url': img_err, 'alt': isRequired('Image alt')})

        if block_data['upload'] and block_data['url']:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'upload': img_err,
                'url': img_err})

        if block_data['url'] and not block_data['alt']:
            error_dict.update({'alt': isRequired('Image Alt')})

        if error_dict:
            raise ValidationError("ImageBasic validation errors", params=error_dict)
        else:
            return block_data
