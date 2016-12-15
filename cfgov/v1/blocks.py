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
