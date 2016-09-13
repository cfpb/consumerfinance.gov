from django.core.exceptions import ValidationError

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from . import atoms
from ..util import util, ref

JS_MOLECULES = []

def isRequired(field_name):
    return [str(field_name) + ' is required.']


class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    sub_heading = blocks.CharBlock(required=False)
    sub_heading_icon = blocks.CharBlock(
        required=False,
        label="Sub heading icon",
        help_text=(
            'A list of icon names can be obtained at: '
            'https://cfpb.github.io/capital-framework/components/cf-icons/. '
            'Examples: linkedin-square, facebook-square, etc.'
            )
        )
    body = blocks.RichTextBlock(blank=True, required=False)
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)

    class Meta:
        icon = 'link'
        template = '_includes/molecules/link-blob.html'


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
        classname = 'block__flush-top'


class Hero(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    background_image = ImageChooserBlock(required=False,
                                         help_text='An image object containing the URL of the image to be placed behind the hero.')

    image = atoms.ImageBasic(required=False)

    background_color = blocks.CharBlock(required=False,
                                        help_text="Use Hexcode colors e.g #F0F8FF")
    links = blocks.ListBlock(atoms.Hyperlink())
    is_button = blocks.BooleanBlock(required=False)
    is_white_text = blocks.BooleanBlock(required=False)
    is_overlay = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/hero.html'
        classname = 'block__flush-top block__flush-bottom'


class FormFieldWithButton(blocks.StructBlock):
    btn_text = blocks.CharBlock(required=False)

    required = blocks.BooleanBlock(required=False)

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

    video = blocks.StructBlock([
        ('id', blocks.CharBlock(required=False, help_text='e.g In \"https://www.youtube.com/watch?v=en0Iq8II4fA\", the ID is everything after the \"?v=\"')),
        ('url', blocks.CharBlock(default='/', required=False)),
        ('height', blocks.CharBlock(default='320', required=False)),
        ('width', blocks.CharBlock(default='568', required=False)),
    ])

    class Meta:
        template = '_includes/molecules/featured-content.html'
        icon = 'doc-full-inverse'
        label = 'Featured Content'
        classname = 'block__flush'


class CallToAction(blocks.StructBlock):
    slug_text = blocks.CharBlock(required=False)
    paragraph_text = blocks.RichTextBlock(required=False)
    button = atoms.Hyperlink()

    class Meta:
        template = '_includes/molecules/call-to-action.html'
        icon = 'grip'
        label = 'Call to action'


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
        icon = 'grip'
        template = '_includes/molecules/related-content.html'
        label = 'Related content'


class Quote(blocks.StructBlock):
    body = blocks.TextBlock()
    citation = blocks.TextBlock()

    class Meta:
        icon = 'openquote'
        template = '_includes/molecules/quote.html'


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
        label = 'Related metadata'


class RSSFeed(blocks.ChoiceBlock):
    choices = [
        ('blog_feed', 'Blog Feed'),
        ('newsroom_feed', 'Newsroom Feed'),
    ]

    class Meta:
        icon = 'plus'
        template = '_includes/molecules/rss-feed.html'
        label = 'RSS feed'


class SocialMedia(blocks.StructBlock):
    is_share_view = blocks.BooleanBlock(default=True,
                                        required=False,
                                        label='Create sharing links',
                                        help_text='If deselected, links to visit CFPB profiles will be created.')
    blurb = blocks.CharBlock(required=False,
                             default='Look what I found on the CFPB\'s site!',
                             help_text='Sets the tweet text, email subject line, and LinkedIn post text.')
    twitter_related = blocks.CharBlock(required=False,
                                       help_text='A comma-separated list of accounts related to the content of the shared URL. Do not enter the @ symbol. If blank, it will default to just "cfpb".')
    twitter_hashtags = blocks.CharBlock(required=False,
                                        help_text='A comma-separated list of hashtags to be appended to default tweet text.')
    twitter_lang = blocks.CharBlock(required=False,
                                    help_text='Loads text components in the specified language, if other than English. E.g., use "es" for Spanish. See https://dev.twitter.com/web/overview/languages for a list of supported language codes.')

    class Meta:
        icon = 'site'
        template = '_includes/molecules/social-media.html'
