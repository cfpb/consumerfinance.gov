from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.safestring import SafeText, mark_safe
from django.utils.text import slugify

from bs4 import BeautifulSoup

from v1.atomic_elements import atoms
from v1.util.util import get_unique_id


try:
    from wagtail.core import blocks
    from wagtail.snippets.blocks import SnippetChooserBlock
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore import blocks
    from wagtail.wagtailsnippets.blocks import SnippetChooserBlock


class AbstractFormBlock(blocks.StructBlock):
    """
    Block class to be subclassed for blocks that involve form handling.
    """
    def get_result(self, page, request, value, is_submitted):
        handler_class = self.get_handler_class()
        handler = handler_class(page, request, block_value=value)
        return handler.process(is_submitted)

    def get_handler_class(self):
        handler_path = self.meta.handler
        if not handler_path:
            raise AttributeError(
                'You must set a handler attribute on the Meta class.')
        return import_string(handler_path)

    def is_submitted(self, request, sfname, index):
        form_id = 'form-%s-%d' % (sfname, index)
        if request.method.lower() == self.meta.method.lower():
            query_dict = getattr(request, self.meta.method.upper())
            return form_id in query_dict.get('form_id', '')
        return False

    class Meta:
        # This should be a dotted path to the handler class for the block.
        handler = None
        method = 'POST'
        icon = 'form'


class AnchorLink(blocks.StructBlock):
    link_id = blocks.CharBlock(
        required=False,
        label='ID for this content block',
        help_text="""
            ID will be auto-generated on save.
            However, you may enter some human-friendly text that
            will be incorporated to make it easier to read.
        """
    )

    def clean(self, data):

        def format_id(string):
            if string == 'anchor':
                return get_unique_id('anchor_')
            elif 'anchor' in string:
                return slugify(string)
            else:
                suffix = '_' if string else ''
                return get_unique_id('anchor_' + slugify(string) + suffix)

        data['link_id'] = format_id(data['link_id'])
        data = super(AnchorLink, self).clean(data)
        return data

    class Meta:
        icon = 'link'
        template = '_includes/atoms/anchor-link.html'
        label = 'Anchor link'


class Feedback(AbstractFormBlock):
    was_it_helpful_text = blocks.CharBlock(
        required=False,
        default='Was this page helpful to you?',
        help_text=(
            'Use this field only for feedback forms '
            'that use "Was this helpful?" radio buttons.'
        )
    )
    intro_text = blocks.CharBlock(
        required=False,
        help_text='Optional feedback intro'
    )
    question_text = blocks.CharBlock(
        required=False,
        help_text='Optional expansion on intro'
    )
    radio_intro = blocks.CharBlock(
        required=False,
        help_text=(
            'Leave blank unless you are building a feedback form with extra '
            'radio-button prompts, as in /owning-a-home/help-us-improve/.'
        )
    )
    radio_text = blocks.CharBlock(
        required=False,
        default='This information helps us understand your question better.'
    )
    radio_question_1 = blocks.CharBlock(
        required=False,
        default='How soon do you expect to buy a home?'

    )
    radio_question_2 = blocks.CharBlock(
        required=False,
        default='Do you currently own a home?'
    )
    button_text = blocks.CharBlock(
        default='Submit'
    )
    contact_advisory = blocks.RichTextBlock(
        required=False,
        help_text='Use only for feedback forms that ask for a contact email'
    )

    class Meta:
        handler = 'v1.handlers.blocks.feedback.FeedbackHandler'
        template = '_includes/blocks/feedback.html'

    class Media:
        js = ['feedback-form.js']


class HeadingIconBlock(blocks.CharBlock):
    classname = 'heading-icon-block'


class HeadingLevelBlock(blocks.ChoiceBlock):
    choices = [
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
    ]
    classname = 'heading-level-block'


class HeadingTextBlock(blocks.CharBlock):
    classname = 'heading-text-block'


class HeadingBlock(blocks.StructBlock):
    text = HeadingTextBlock(required=False)
    level = HeadingLevelBlock(default='h2')
    icon = HeadingIconBlock(
        required=False,
        help_text=mark_safe(
            'Input the name of an icon to appear to the left of the heading. '
            'E.g., approved, help-round, etc. '
            '<a href="https://cfpb.github.io/capital-framework/'
            'components/cf-icons/#the-icons">See full list of icons</a>'
        ),
    )

    class Meta:
        icon = 'title'
        template = '_includes/blocks/heading.html'
        form_template = (
            'admin/form_templates/struct-with-block-wrapper-classes.html'
        )


class PlaceholderFieldBlock(blocks.FieldBlock):
    def __init__(self, *args, **kwargs):
        super(PlaceholderFieldBlock, self).__init__(*args, **kwargs)
        self.placeholder = kwargs.pop('placeholder', None)

    def render_form(self, *args, **kwargs):
        html = super(PlaceholderFieldBlock, self).render_form(*args, **kwargs)

        if self.placeholder is not None:
            html = self.replace_placeholder(html, self.placeholder)

        return html

    @staticmethod
    def replace_placeholder(html, placeholder):
        soup = BeautifulSoup(html, 'html.parser')
        inputs = soup.findAll('input')

        if 1 != len(inputs):
            raise ValueError('block must contain a single input tag')

        inputs[0]['placeholder'] = placeholder

        return SafeText(soup)


class PlaceholderCharBlock(PlaceholderFieldBlock, blocks.CharBlock):
    pass


class ReusableTextChooserBlock(SnippetChooserBlock):
    class Meta:
        template = '_includes/snippets/reusable_text.html'


class Link(blocks.StructBlock):
    link_text = blocks.CharBlock(
        required=True,
        label='Text'
    )
    page_link = blocks.PageChooserBlock(
        required=False,
        help_text='Link to a page in Wagtail.',
        label='Page'
    )
    external_link = blocks.CharBlock(
        required=False,
        max_length=1000,
        label='Direct URL (rare)',
        help_text='Enter url for page outside Wagtail. This will only '
                  'be used if there is no page selected.'
    )

    def clean(self, value):
        cleaned = super(Link, self).clean(value)

        if not cleaned.get('page_link') and not cleaned.get('external_link'):
            raise ValidationError(
                'Validation error in link',
                params={
                    'page_link': [
                        'Either page or external link is required.'
                    ],
                    'external_link': [
                        'Either page or external link is required.'
                    ]
                }
            )
        return cleaned


class NavItem(blocks.StructBlock):
    state = blocks.ChoiceBlock(choices=[
        ('both', 'Show always'),
        ('live', 'Show on Production only'),
        ('draft', 'Show on Content only')],
        default='both',
        help_text='Select state for this link. Test new links '
                  'by setting them to only show on Content.')
    link = Link(required=False)
    nav_items = blocks.ListBlock(
        blocks.StructBlock([
            ('link', Link())
        ]),
        label='Child items (mobile only)'
    )


class NavGroup(blocks.StructBlock):
    draft = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='If checked, this block will only show '
        'on our sharing site (Content).',
        label='Mark block as draft'
    )
    group_title = blocks.CharBlock(
        required=False,
        label='Column title')
    hide_group_title = blocks.BooleanBlock(
        required=False,
        label='Hide column title',
        help_text='If column shares title with previous column, '
                  'enter title text above but check this box so title '
                  'only shows in first column.')
    nav_items = blocks.ListBlock(
        NavItem(),
        required=False,
        label='Menu items')


class NavFooter(blocks.StructBlock):
    draft = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text='If checked, this block will only show '
        'on our sharing site (Content).',
        label='Mark block as draft'
    )
    content = blocks.RichTextBlock(
        required=False,
        features=['link']
    )


class FeaturedMenuContent(blocks.StructBlock):
    draft = blocks.BooleanBlock(
        required=False,
        default=False,
        label='Mark block as draft',
        help_text='If checked, this block will only show '
        'on our sharing site (Content).'
    )
    link = Link(required=False, label="H4 link")
    body = blocks.RichTextBlock(required=False)
    image = atoms.ImageBasic(required=False)
