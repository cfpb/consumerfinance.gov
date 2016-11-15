from django.utils.module_loading import import_string
from django.utils.text import slugify
from wagtail.wagtailcore import blocks

from .util.util import get_unique_id


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
        help_text=(
                'Auto-generated on save, or enter some human-friendly text ',
                'to make it easier to read.'
            )
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
            'Leave blank for anything but a "Was this helpful" '
            'radio-button feedback form.'
            )
        )
    intro_text = blocks.CharBlock(
        required=False,
        default='Provide additional feedback'
        )
    question_text = blocks.CharBlock(
        required=False,
        default=(
            'Have any additional feedback about the page you were just on? '
            'Please use the form below to share your thoughts.'),
        help_text=(
            'Leave blank unless you are building a referred-page '
            'feedback form, as in /owning-a-home/feedback/.')
    )
    optional_intro = blocks.CharBlock(
        required=False,
        default='Optional: Tell us a bit more about yourself.',
        help_text=(
            'Leave blank unless you are building a feedback form with extra '
            'radio-button prompts, as in /owning-a-home/help-us-improve/.'
            )
    )
    optional_text = blocks.CharBlock(
        required=False,
        default='This information helps us understand your question better.'
    )
    optional_question_1 = blocks.CharBlock(
        required=False,
        default='How soon do you expect to buy a home?'

    )
    optional_question_2 = blocks.CharBlock(
        required=False,
        default='Do you currently own a home?'
    )
    button_text = blocks.CharBlock(default='Submit')

    class Meta:
        handler = 'v1.handlers.blocks.feedback.FeedbackHandler'
        template = '_includes/blocks/feedback.html'
