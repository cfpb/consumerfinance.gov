from wagtail.wagtailcore import blocks
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock

from . import atoms
from . import molecules
from .snippets import Contact as ContactSnippetClass


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

    class Meta:
        icon = 'mail'
        template = '_includes/organisms/email-signup.html'


class RelatedPosts(blocks.StructBlock):
    limit = blocks.CharBlock(default='3', label='Limit')
    relate_posts = blocks.BooleanBlock(required=False, default=True, label='Blog Posts')
    relate_newsroom = blocks.BooleanBlock(required=False, default=True, label='Newsroom')
    relate_events = blocks.BooleanBlock(required=False, default=True, label='Events')
    view_more = atoms.Hyperlink(required=False)

    class Meta:
        icon = 'link'
        template = '_includes/molecules/related-posts.html'


class MainContactInfo(blocks.StructBlock):
    header = blocks.CharBlock()
    body = blocks.RichTextBlock()
    contact = SnippetChooserBlock(ContactSnippetClass)

    class Meta:
        icon = 'wagtail'
        template = '_includes/organisms/main-contact-info.html'
