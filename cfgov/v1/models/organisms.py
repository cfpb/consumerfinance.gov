from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from . import atoms
from . import molecules


class Well(blocks.StructBlock):
    content = blocks.RichTextBlock(required=True)

    class Meta:
        icon = 'title'
        template = '_includes/organisms/well.html'


class FullWidthText(blocks.StructBlock):
    content = blocks.RichTextBlock(required=True)

    class Meta:
        icon = 'title'
        template = '_includes/organisms/full-width-text.html'


class PostPreview(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100, required=True)
    body = blocks.RichTextBlock(required=True)
    image = atoms.ImageBasic(required=False)

    post = blocks.PageChooserBlock(required=True)

    link = atoms.Hyperlink(required=False)

    class Meta:
        icon = 'view'
        template = '_includes/organisms/post-preview.html'


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
