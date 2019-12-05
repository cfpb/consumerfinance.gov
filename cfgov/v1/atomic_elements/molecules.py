from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from v1.atomic_elements import atoms
from v1.blocks import AnchorLink, HeadingBlock
from v1.feeds import get_appropriate_rss_feed_url_for_page


class HalfWidthLinkBlob(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, label="H3 heading")
    sub_heading = blocks.CharBlock(required=False, label="H4 heading")
    sub_heading_icon = blocks.CharBlock(
        required=False,
        label="H4 heading icon",
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


class InfoUnit(blocks.StructBlock):
    image = atoms.ImageBasic(
        required=False,
    )

    heading = HeadingBlock(
        required=False,
        default={'level': 'h3'}
    )

    body = blocks.RichTextBlock(blank=True, required=False)
    links = blocks.ListBlock(atoms.Hyperlink(), required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/info-unit.html'


class ImageText5050(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(blank=True, required=False)
    image = atoms.ImageBasic()
    is_widescreen = blocks.BooleanBlock(required=False, label="Use 16:9 image")
    is_button = blocks.BooleanBlock(required=False,
                                    label="Show links as button")
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
    eyebrow = blocks.CharBlock(
        required=False,
        help_text=('Optional: Adds an H5 eyebrow above H1 heading text. '
                   'Only use in conjunction with heading.'),
        label='Pre-heading'
    )
    heading = blocks.CharBlock(required=False)
    intro = blocks.RichTextBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    links = blocks.ListBlock(atoms.Hyperlink(required=False), required=False)
    has_rule = blocks.BooleanBlock(
        required=False,
        label="Has bottom rule",
        help_text=('Check this to add a horizontal rule line to bottom of '
                   'text introduction.')
    )

    def clean(self, value):
        cleaned = super(TextIntroduction, self).clean(value)

        # Eyebrow requires a heading.
        if cleaned.get('eyebrow') and not cleaned.get('heading'):
            raise ValidationError(
                'Validation error in TextIntroduction: '
                'pre-heading requires heading',
                params={'heading': ErrorList([
                    'Required if a pre-heading is entered.'
                ])}
            )

        return cleaned

    class Meta:
        icon = 'title'
        template = '_includes/molecules/text-introduction.html'
        classname = 'block__flush-top'


class Hero(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=False,
        help_text=mark_safe(
            'For complete guidelines on creating heroes, visit our '
            '<a href="https://cfpb.github.io/design-manual/global-elements/heroes.html">'  # noqa: E501
            'Design Manual</a>.'
            '<ul class="help">Character counts (including spaces) at largest '
            'breakpoint:'
            '<li>&bull; 41 characters max (one-line heading)</li>'
            '<li>&bull; 82 characters max (two-line heading)</li></ul>')
    )
    body = blocks.RichTextBlock(
        label="Sub-heading",
        required=False,
        help_text=mark_safe(
            '<ul class="help">Character counts (including spaces) at largest '
            'breakpoint:'
            '<li>&bull; 165-186 characters (after a one-line heading)</li>'
            '<li>&bull; 108-124 characters (after a two-line heading)</li>'
            '</ul>')
    )
    image = ImageChooserBlock(
        label="Large image",
        required=False,
        help_text=mark_safe(
            'When saving illustrations, use a transparent background. '
            '<a href="https://cfpb.github.io/design-manual/global-elements/heroes.html#style">'  # noqa: E501
            'See image dimension guidelines.</a>')
    )
    small_image = ImageChooserBlock(
        required=False,
        help_text=mark_safe(
            '<b>Optional.</b> Provides an alternate image for '
            'small displays when using a photo or bleeding hero. '
            'Not required for the standard illustration. '
            '<a href="https://cfpb.github.io/design-manual/global-elements/heroes.html#style">'  # noqa:E501
            'See image dimension guidelines.</a>')
    )
    background_color = blocks.CharBlock(
        required=False,
        help_text=mark_safe(
            'Specify a hex value (with the # sign) from our '
            '<a href="https://cfpb.github.io/design-manual/brand-guidelines/color-principles.html">'  # noqa: E501
            'official color palette</a>.')
    )
    is_overlay = blocks.BooleanBlock(
        label="Photo",
        required=False,
        help_text=mark_safe(
            '<b>Optional.</b> Uses the large image as a background under '
            'the entire hero, creating the "Photo" style of hero (see '
            '<a href="https://cfpb.github.io/design-manual/global-elements/heroes.html">'  # noqa: E501
            'Design Manual</a> for details). When using this option, '
            'make sure to specify a background color (above) for the '
            'left/right margins that appear when screens are wider than '
            '1200px and for the text section when the photo and text '
            'stack at mobile sizes.')
    )
    is_white_text = blocks.BooleanBlock(
        label="White text",
        required=False,
        help_text=mark_safe(
            '<b>Optional.</b> Turns the hero text white. Useful if using '
            'a dark background color or background image.')
    )
    is_bleeding = blocks.BooleanBlock(
        label="Bleed",
        required=False,
        help_text=mark_safe(
            '<b>Optional.</b> Select if you want the illustration to bleed '
            'vertically off the top and bottom of the hero space.')
    )

    class Meta:
        icon = 'image'
        template = '_includes/molecules/hero.html'
        classname = 'block__flush-top block__flush-bottom'


class Notification(blocks.StructBlock):
    message = blocks.CharBlock(
        required=True,
        help_text='The main notification message to display.'
    )
    explanation = blocks.TextBlock(
        required=False,
        help_text='Explanation text appears below the message in smaller type.'
    )
    links = blocks.ListBlock(
        atoms.Hyperlink(required=False),
        required=False,
        help_text='Links appear on their own lines below the explanation.'
    )

    class Meta:
        icon = 'warning'
        template = '_includes/molecules/notification.html'


class CallToAction(blocks.StructBlock):
    slug_text = blocks.CharBlock(required=False)
    paragraph_text = blocks.RichTextBlock(required=False)
    button = atoms.Button()

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


def phone_number_format_validator():
    return RegexValidator(
        regex=r'^\d*$',
        message="Enter a numeric phone number, without punctuation.")


class ContactPhone(blocks.StructBlock):
    fax = blocks.BooleanBlock(default=False, required=False,
                              label='Is this number a fax?')
    phones = blocks.ListBlock(
        blocks.StructBlock([
            ('number', blocks.CharBlock(
                max_length=15,
                help_text='Do not include spaces or dashes. Ex. 8554112372',
                validators=[phone_number_format_validator()]
            )),
            ('extension', blocks.CharBlock(max_length=4, required=False)),
            ('vanity', blocks.CharBlock(
                max_length=15,
                required=False,
                help_text='A phoneword version of the above number. '
                          'Include any formatting. Ex. (555) 222-CFPB'
            )),
            ('tty', blocks.CharBlock(
                max_length=15,
                required=False,
                label="TTY",
                help_text='Do not include spaces or dashes. Ex. 8554112372',
                validators=[phone_number_format_validator()]
            )),
            ('tty_ext', blocks.CharBlock(
                max_length=4,
                required=False,
                label="TTY Extension"
            )),
        ]))

    class Meta:
        icon = 'mail'
        template = '_includes/molecules/contact-phone.html'
        label = 'Phone'


class ContentImage(blocks.StructBlock):
    image = atoms.ImageBasic()
    image_width = blocks.ChoiceBlock(
        choices=[('full', 'full'),
                 (470, '470px'),
                 (270, '270px'),
                 (170, '170px')],
        default='full',)
    image_position = blocks.ChoiceBlock(
        choices=[('right', 'right'),
                 ('left', 'left')],
        default='right',
        help_text='Does not apply if the image is full-width',
    )
    text = blocks.RichTextBlock(required=False, label='Caption')
    is_bottom_rule = blocks.BooleanBlock(
        required=False,
        default=True,
        label='Has bottom rule line',
        help_text='Check to add a horizontal rule line to bottom of inset.'
    )

    class Meta:
        icon = 'image'
        template = '_includes/molecules/content-image.html'
        label = 'Image'


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
    citation = blocks.TextBlock(required=False)
    is_large = blocks.BooleanBlock(required=False)

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
            ('date', blocks.DateBlock())
        ], icon='date')),
        ('topics', blocks.StructBlock([
            ('heading', blocks.CharBlock(max_length=100, default='Topics')),
            ('show_topics', blocks.BooleanBlock(default=True, required=False))
        ], icon='tag')),
        ('categories', blocks.StructBlock([
            ('heading', blocks.CharBlock(
                max_length=100,
                default='Categories'
            )),
            ('show_categories', blocks.BooleanBlock(
                default=True,
                required=False
            ))
        ], icon='list-ul')),
    ])
    is_half_width = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = 'grip'
        template = '_includes/molecules/related-metadata.html'
        label = 'Related metadata'


class RSSFeed(blocks.StaticBlock):
    class Meta:
        icon = 'plus'
        template = '_includes/molecules/rss-feed.html'
        label = 'RSS feed'
        admin_text = mark_safe(
            '<h3>RSS Feed</h3>'
            'If this page or one of its ancestors provides an RSS feed, '
            'this block renders a link to that feed. If not, this block '
            'renders nothing.'
        )

    def get_context(self, value, parent_context=None):
        context = super(RSSFeed, self).get_context(
            value,
            parent_context=parent_context
        )

        page = context.get('page')

        if page:
            context['value'] = get_appropriate_rss_feed_url_for_page(page)

        return context


class SocialMedia(blocks.StructBlock):
    is_share_view = blocks.BooleanBlock(
        default=True,
        required=False,
        label='Desired action: share this page',
        help_text='If unchecked, social media icons will link users to '
                  'official CFPB accounts. Do not fill in any further fields.'
    )

    blurb = blocks.CharBlock(
        required=False,
        default="Look what I found on the CFPB's site!",
        help_text='Sets the tweet text, email subject line, '
                  'and LinkedIn post text.'
    )

    twitter_text = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text='(Optional) Custom text for Twitter shares. If blank, '
                  'will default to value of blurb field above.'
    )
    twitter_related = blocks.CharBlock(
        required=False,
        help_text='(Optional) A comma-separated list of accounts related '
                  'to the content of the shared URL. Do not enter the '
                  ' @ symbol. If blank, it will default to just "cfpb".'
    )
    twitter_hashtags = blocks.CharBlock(
        required=False,
        help_text='(Optional) A comma-separated list of hashtags to be '
                  'appended to default tweet text.'
    )
    twitter_lang = blocks.CharBlock(
        required=False,
        help_text='(Optional) Loads text components in the specified '
                  'language, if other than English. E.g., use "es" '
                  ' for Spanish. '
                  'See https://dev.twitter.com/web/overview/languages '
                  'for a list of supported language codes.'
    )

    email_title = blocks.CharBlock(
        required=False,
        help_text='(Optional) Custom subject for email shares. If blank, '
                  'will default to value of blurb field above.'
    )

    email_text = blocks.CharBlock(
        required=False,
        help_text='(Optional) Custom text for email shares. If blank, will '
                  'default to "Check out this page from the CFPB".'
    )

    email_signature = blocks.CharBlock(
        required=False,
        help_text='(Optional) Adds a custom signature line to email shares. '
    )
    linkedin_title = blocks.CharBlock(
        required=False,
        help_text='(Optional) Custom title for LinkedIn shares. If blank, '
                  'will default to value of blurb field above.'
    )

    linkedin_text = blocks.CharBlock(
        required=False,
        help_text='(Optional) Custom text for LinkedIn shares.'
    )

    class Meta:
        icon = 'site'
        template = '_includes/molecules/social-media.html'


class ContentWithAnchor(blocks.StructBlock):
    content_block = blocks.RichTextBlock()
    anchor_link = AnchorLink()

    class Meta:
        icon = 'edit'
        template = '_includes/molecules/full-width-text-anchor.html'
