from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from . import molecules


class Well(blocks.StructBlock):
    content = blocks.RichTextBlock(required=True)

    class Meta:
        icon = 'title'
        template = '_includes/organisms/well.html'


class EmailSignUp(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    text = blocks.CharBlock(required=True)
    gd_code = blocks.CharBlock(required=False)

    form_field = blocks.ListBlock(molecules.FormFieldWithButton(), icon='mail', required=False)

    panels = [
        FieldPanel('text'),
        FieldPanel('gd_code'),
        FieldPanel('form_field'),
    ]

    class Meta:
        icon = 'mail'
        template = '_includes/organisms/email-signup.html'
