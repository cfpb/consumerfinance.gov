from django import forms

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from url_or_relative_url_field.forms import URLOrRelativeURLFormField


def is_required(field_name):
    return [str(field_name) + ' is required.']


class URLOrRelativeURLBlock(blocks.FieldBlock):
    def __init__(
        self, required=True, help_text=None, max_length=None, min_length=None,
        validators=(), **kwargs
    ):
        self.field = URLOrRelativeURLFormField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            validators=validators,
        )
        super().__init__(**kwargs)

    class Meta:
        icon = 'site'


class Hyperlink(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    aria_label = blocks.CharBlock(
        required=False,
        help_text='Add an ARIA label if the link text does not describe the '
                  'destination of the link (e.g. has ambiguous text like '
                  '"Learn more" that is not descriptive on its own).'
    )
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
        except StructBlockValidationError as e:
            error_dict.update(e.block_errors)

        if self.required:
            if not data['text']:
                error_dict.update({'text': is_required('Text')})

        if error_dict:
            raise StructBlockValidationError(block_errors=error_dict)
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


class ImageBasicStructValue(blocks.StructValue):
    @property
    def url(self):
        upload = self.get('upload')

        if upload:
            return upload.get_rendition('original').url

    @property
    def alt_text(self):
        # TODO: This duplicates the logic in v1.jinja2tags.image_alt_value,
        # which cannot be called here because of a circular import. It would
        # be better to deprecate the image_alt_value tag in favor of using
        # this logic wherever we use ImageBasic atoms.
        alt = self.get('alt')
        if alt:
            return alt

        upload = self.get('upload')
        if upload:
            return upload.alt

        # If this block has no upload defined, its alt text is undefined.
        return None


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
        except StructBlockValidationError as e:
            error_dict.update(e.block_errors)

        if not self.required and not data['upload']:
            return data

        if not data['upload']:
            error_dict.update({'upload': is_required("Upload")})

        if error_dict:
            raise StructBlockValidationError(block_errors=error_dict)
        else:
            return data

    class Meta:
        icon = 'image'
        value_class = ImageBasicStructValue
