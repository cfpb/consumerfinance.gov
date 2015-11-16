from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from . import molecules


class Well(blocks.StructBlock):
    template_path = blocks.CharBlock(required=True)

    class Meta:
        icon = 'link'
        template = 'v1/demo/organisms/well.html'


class EmailSignUp(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    gd_code = blocks.CharBlock(required=False)

    signup = StreamField([
        ('signup_button', molecules.FormFieldWithButton()),
    ], blank=True)

    panels = [
        FieldPanel('text'),
        FieldPanel('gd_code'),
        StreamFieldPanel('signup'),
    ]

    class Meta:
        icon = 'link'
        template = 'v1/demo/organisms/email-signup.html'
