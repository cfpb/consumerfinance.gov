import re

from django import forms
from django.core.exceptions import ValidationError


try:
    from wagtail.core import blocks
    from wagtail.images.blocks import ImageChooserBlock
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore import blocks
    from wagtail.wagtailimages.blocks import ImageChooserBlock


def number_validator(value, search=re.compile(r'[^0-9]').search):
    if value:
        return bool(search(value))
    else:
        return False


def is_required(field_name):
    return [str(field_name) + ' is required.']


class NumberBlock(blocks.StructBlock):
    text = blocks.CharBlock(max_length=100, required=False)

    def __init__(self, required=True):
        self.is_required = required
        super(NumberBlock, self).__init__()

    @property
    def required(self):
        return self.is_required

    def clean(self, data):
        error_dict = {}

        try:
            data = super(NumberBlock, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if self.required:
            if not data['text']:
                error_dict.update({'text': is_required('Text')})

        if number_validator(data['text']):
            error_dict.update({'text': ['Must be a numerical value']})

        if error_dict:
            raise ValidationError("NumberBlock validation errors",
                                  params=error_dict)
        else:
            return data

    class Meta:
        icon = 'order'
        template = '_includes/atoms/number.html'


class IntegerBlock(blocks.FieldBlock):
    def __init__(self, required=True, help_text=None, min_value=None,
                 max_value=None, **kwargs):
        self.field = forms.IntegerField(
            required=required,
            help_text=help_text,
            min_value=min_value,
            max_value=max_value
        )
        super(IntegerBlock, self).__init__(**kwargs)

    class Meta:
        icon = 'plus-inverse'


class Hyperlink(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    url = blocks.CharBlock(default='/', required=False)

    def __init__(self, required=True):
        self.is_required = required
        super(Hyperlink, self).__init__()

    @property
    def required(self):
        return self.is_required

    def clean(self, data):
        error_dict = {}

        try:
            data = super(Hyperlink, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if self.required:
            if not data['text']:
                error_dict.update({'text': is_required('Text')})

        if error_dict:
            raise ValidationError("Hyperlink validation errors",
                                  params=error_dict)
        else:
            return data

    class Meta:
        icon = 'link'
        template = '_includes/atoms/hyperlink.html'


class Button(Hyperlink):
    size = blocks.ChoiceBlock(choices=[
        ('regular', 'Regular'),
        ('large', 'Large Primary'),
    ], default='regular')


class ImageBasic(blocks.StructBlock):
    upload = ImageChooserBlock(required=False)
    alt = blocks.CharBlock(
        required=False,
        help_text='If the image is decorative (i.e., if a screenreader '
                  'wouldn\'t have anything useful to say about it), leave the '
                  'Alt field blank.'
    )

    def __init__(self, required=True):
        self.is_required = required
        super(ImageBasic, self).__init__()

    @property
    def required(self):
        return self.is_required

    def clean(self, data):
        error_dict = {}

        try:
            data = super(ImageBasic, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if not self.required and not data['upload']:
            return data

        if not data['upload']:
            error_dict.update({'upload': is_required("Upload")})

        if error_dict:
            raise ValidationError("ImageBasic validation errors",
                                  params=error_dict)
        else:
            return data

    class Meta:
        icon = 'image'


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
            error_dict.update({
                'upload': img_err,
                'url': img_err,
                'alt': is_required('Image alt')
            })

        if data['upload'] and data['url']:
            img_err = ['Please select one method of image rendering']
            error_dict.update({
                'upload': img_err,
                'url': img_err})

        if error_dict:
            raise ValidationError("ImageBasicUrlAlt validation errors",
                                  params=error_dict)
        else:
            return data
