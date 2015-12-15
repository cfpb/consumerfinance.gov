from django.core.exceptions import ValidationError

from wagtail.wagtailcore import blocks

from . import atoms

from ..util import id_validator


def isRequired(field_name):
    return [str(field_name) + ' is required.']


class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(blank=True)
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)

    class Meta:
        icon = 'link'
        template = '_includes/molecules/half-width-link-blob.html'


class ImageText5050(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(blank=True)
    image = atoms.ImageBasic()
    is_widescreen = blocks.BooleanBlock(required=False, label="Use 16:9 image")
    is_button = blocks.BooleanBlock(required=False, label="Show links as button")
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/image-text-50-50.html'


class ImageText2575(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=True)
    image = atoms.ImageBasicAlt()
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/image-text-25-75.html'


class TextIntroduction(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    intro = blocks.RichTextBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    links = blocks.ListBlock(atoms.Hyperlink(required=False), required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'title'
        template = '_includes/molecules/text-introduction.html'


class Hero(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=False)

    image = atoms.ImageBasic()

    background_color = blocks.CharBlock(max_length=100, required=False)
    link = atoms.Hyperlink(required=False)
    is_button = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/hero.html'


class FormFieldWithButton(blocks.StructBlock):
    btn_text = blocks.CharBlock(max_length=100, required=True)

    required = blocks.BooleanBlock(required=False)
    id = blocks.CharBlock(max_length=100, required=True)
    info = blocks.RichTextBlock(required=False, label="Disclaimer")
    label = blocks.CharBlock(max_length=100, required=True)
    type = blocks.ChoiceBlock(choices=[
        ('text', 'Text'),
        ('checkbox', 'Checkbox'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('url', 'URL'),
        ('radio', 'Radio'),
    ], required=True)
    placeholder = blocks.CharBlock(max_length=100, required=False)

    def clean(self, data):
        error_dict = {}

        try:
            data = super(FormFieldWithButton, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if not id_validator(data['id']):
            id_err = ['Id must only contain alphabets, numbers, underscores and hyphens']
            error_dict.update({'id': id_err})

        if error_dict:
            raise ValidationError("ImageBasicUrlAlt validation errors", params=error_dict)
        else:
            return data

    class Meta:
        icon = 'mail'
        template = '_includes/molecules/form-field-with-button.html'


class CallToAction(blocks.StructBlock):
    slug_text = blocks.CharBlock(max_length=100, required=True)
    paragraph_text = blocks.RichTextBlock(required=True)
    button = atoms.Hyperlink()

    class Meta:
        template = '_includes/molecules/call-to-action.html'
        icon = 'grip'
        label = 'Call to Action'


class ContactAddress(blocks.StructBlock):
    label = blocks.CharBlock(max_length=50)
    title = blocks.CharBlock(max_length=100, required=False)
    street = blocks.CharBlock(max_length=100)
    city = blocks.CharBlock(max_length=50)
    state = blocks.CharBlock(max_length=25)
    zip_code = blocks.CharBlock(max_length=15, required=False)

    class Meta:
        template = '_includes/molecules/contact-address.html'
        icon = 'mail'
        label = 'Address'


class ContactEmail(blocks.StructBlock):
    emails = blocks.ListBlock(atoms.Hyperlink())

    class Meta:
        icon = 'mail'
        template = '_includes/molecules/contact-email.html'
        label = 'Email'


class ContactPhone(blocks.StructBlock):
    fax = blocks.BooleanBlock(default=False, required=False,
                              label='Is this number a fax?')
    phones = blocks.ListBlock(
        blocks.StructBlock([
            ('number', blocks.CharBlock(max_length=15)),
            ('vanity', blocks.CharBlock(max_length=15, required=False)),
            ('tty', blocks.CharBlock(max_length=15, required=False)),
        ]))

    class Meta:
        icon = 'mail'
        template = '_includes/molecules/contact-phone.html'
        label = 'Phone'


class Expandable(blocks.StructBlock):
    label = blocks.CharBlock(max_length=100, required=False)
    paragraph = blocks.RichTextBlock(required=False)

    optional_content = blocks.StreamBlock(
        [
            ('links', atoms.Hyperlink()),
            ('email', ContactEmail()),
            ('phone', ContactPhone()),
            ('address', ContactAddress()),
        ], blank=True
    )

    is_bordered = blocks.BooleanBlock(required=False)
    is_midtone = blocks.BooleanBlock(required=False)
    is_expanded = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'list-ul'
        template = '_includes/molecules/expandable.html'
        label = 'Expandable'
