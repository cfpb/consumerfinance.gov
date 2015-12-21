from django.core.exceptions import ValidationError

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


def isRequired(field_name):
    return [str(field_name) + ' is required.']


class Hyperlink(blocks.StructBlock):
    text = blocks.CharBlock(max_length=100, required=False)
    url = blocks.CharBlock(default='/', required=False)

    def __init__(self, required=True):
        self.required = required
        super(Hyperlink, self).__init__()

    def clean(self, data):
        error_dict = {}

        try:
            data = super(Hyperlink, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if self.required:
            if not data['text']:
                error_dict.update({'text': isRequired('Text')})

        if error_dict:
            raise ValidationError("Hyperlink validation errors", params=error_dict)
        else:
            return data

    class Meta:
        icon = 'link'
        template = '_includes/atoms/hyperlink.html'


class ImageBasic(blocks.StructBlock):
    upload = ImageChooserBlock(required=False)
    alt = blocks.CharBlock(required=False)

    def __init__(self, required=True):
        self.required = required
        super(ImageBasic, self).__init__()

    def clean(self, data):
        error_dict = {}

        try:
            data = super(ImageBasic, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if not self.required and not data['upload']:
            return data

        if not data['upload']:
            error_dict.update({'upload': isRequired("Upload")})

        if error_dict:
            raise ValidationError("ImageBasic validation errors", params=error_dict)
        else:
            return data


class ImageBasicUrl(ImageBasic):
    url = blocks.CharBlock(required=False)

    def clean(self, data):
        error_dict = {}

        try:
            data = super(ImageBasicUrl, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if not self.required and not data['upload'] and not data['url']:
            return data

        if not data['upload'] and not data['url']:
            img_err = ['Please upload or enter an image path']
            error_dict.update({'upload': img_err, 'url': img_err, 'alt': isRequired('Image alt')})

        if data['upload'] and data['url']:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'upload': img_err,
                'url': img_err})

        if error_dict:
            raise ValidationError("ImageBasicUrlAlt validation errors", params=error_dict)
        else:
            return data