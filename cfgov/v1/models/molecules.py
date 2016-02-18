from django.core.exceptions import ValidationError

from wagtail.wagtailcore import blocks

from . import ref
from . import atoms
from ..util import util


def isRequired(field_name):
    return [str(field_name) + ' is required.']


class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(blank=True, required=False)
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)

    class Meta:
        icon = 'link'
        template = '_includes/molecules/half-width-link-blob.html'


class ImageText5050(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(blank=True, required=False)
    image = atoms.ImageBasic()
    is_widescreen = blocks.BooleanBlock(required=False, label="Use 16:9 image")
    is_button = blocks.BooleanBlock(required=False, label="Show links as button")
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/image-text-50-50.html'


class ImageText2575(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    image = atoms.ImageBasic()
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/image-text-25-75.html'


class TextIntroduction(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    intro = blocks.RichTextBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    links = blocks.ListBlock(atoms.Hyperlink(required=False), required=False)
    has_rule = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'title'
        template = '_includes/molecules/text-introduction.html'


class Hero(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    image = atoms.ImageBasic()

    background_color = blocks.CharBlock(required=False,
                                        help_text="Use Hexcode colors e.g #F0F8FF")
    links = blocks.ListBlock(atoms.Hyperlink())
    is_button = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/hero.html'


class FormFieldWithButton(blocks.StructBlock):
    btn_text = blocks.CharBlock(required=False)

    required = blocks.BooleanBlock(required=False)
    id = blocks.CharBlock(required=False,
                          help_text="Type of form i.e emailForm, submission-form. Should be unique if multiple forms are used")
    info = blocks.RichTextBlock(required=False, label="Disclaimer")
    label = blocks.CharBlock(required=True)
    type = blocks.ChoiceBlock(choices=[
        ('text', 'Text'),
        ('checkbox', 'Checkbox'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('url', 'URL'),
        ('radio', 'Radio'),
    ], required=False)
    placeholder = blocks.CharBlock(required=False)

    def clean(self, data):
        error_dict = {}

        try:
            data = super(FormFieldWithButton, self).clean(data)
        except ValidationError as e:
            error_dict.update(e.params)

        if not util.id_validator(data['id']):
            id_err = ['Id must only contain alphabets, numbers, underscores and hyphens']
            error_dict.update({'id': id_err})

        if error_dict:
            raise ValidationError("ImageBasicUrlAlt validation errors", params=error_dict)
        else:
            return data

    class Meta:
        icon = 'mail'
        template = '_includes/molecules/form-field-with-button.html'


class FeaturedContent(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    category = blocks.ChoiceBlock(choices=ref.fcm_types, required=False)
    post = blocks.PageChooserBlock(required=False)

    show_post_link = blocks.BooleanBlock(required=False, label="Render post link?")
    post_link_text = blocks.CharBlock(required=False)

    image = atoms.ImageBasic(required=False)
    links = blocks.ListBlock(atoms.Hyperlink(required=False),
                             label='Additional Links')

    class Meta:
        template = '_includes/molecules/featured-content.html'
        icon = 'doc-full-inverse'
        label = 'Featured Content'


class CallToAction(blocks.StructBlock):
    slug_text = blocks.CharBlock(required=False)
    paragraph_text = blocks.RichTextBlock(required=False)
    button = atoms.Hyperlink()

    class Meta:
        template = '_includes/molecules/call-to-action.html'
        icon = 'grip'
        label = 'Call to Action'


class ContactAddress(blocks.StructBlock):
    label = blocks.CharBlock(required=False)
    title = blocks.CharBlock(required=False)
    street = blocks.CharBlock(required=False)
    city = blocks.CharBlock(max_length=50, required=False)
    state = blocks.CharBlock(max_length=25, required=False)
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


class RelatedLinks(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    paragraph = blocks.RichTextBlock(required=False)
    links = blocks.ListBlock(atoms.Hyperlink())

    class Meta:
        icon = 'link'
        template = '_includes/molecules/related-links.html'


class Quote(blocks.StructBlock):
    body = blocks.TextBlock()
    citation = blocks.TextBlock()

    class Meta:
        icon = 'openquote'
        template = '_includes/molecules/quote.html'


class BaseExpandable(blocks.StructBlock):
    label = blocks.CharBlock(required=False)
    is_bordered = blocks.BooleanBlock(required=False)
    is_midtone = blocks.BooleanBlock(required=False)
    is_expanded = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'list-ul'
        template = '_includes/molecules/expandable.html'
        label = 'Expandable'

    class Media:
        js = ("expandable.js",)


class Expandable(BaseExpandable):
    content = blocks.StreamBlock(
        [
            ('paragraph', blocks.RichTextBlock(required=False)),
            ('links', atoms.Hyperlink()),
            ('email', ContactEmail()),
            ('phone', ContactPhone()),
            ('address', ContactAddress()),
        ], blank=True
    )


class RelatedMetadata(blocks.StructBlock):
    slug = blocks.CharBlock(max_length=100)
    content = blocks.StreamBlock([
        ('text', blocks.StructBlock([
            ('heading', blocks.CharBlock(max_length=100)),
            ('blob', blocks.RichTextBlock())
        ], icon='pilcrow')),
        ('list', blocks.StructBlock([
            ('heading', blocks.CharBlock(max_length=100)),
            ('links', blocks.ListBlock(atoms.Hyperlink())),
        ], icon='list-ul')),
        ('date', blocks.StructBlock([
            ('heading', blocks.CharBlock(max_length=100)),
            ('date', blocks.DateBlock(required=False))
        ], icon='date')),
        ('topics', blocks.StructBlock([
            ('heading', blocks.CharBlock(max_length=100, default='Topics')),
            ('show_topics', blocks.BooleanBlock(default=True, required=False))
        ], icon='tag')),
    ])
    half_width = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'grip'
        template = '_includes/molecules/related-metadata.html'
        label = 'Related Metadata'
