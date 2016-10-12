from django.core.exceptions import ValidationError
from wagtail.wagtailcore import blocks
from django.utils.module_loading import import_string
from django.utils.text import slugify
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
    link_id = blocks.CharBlock(required=False, label='ID for this content block', help_text=(
            'Auto-generated on save, or enter some human-friendly text to make it easier to read.'
            )
        )

    # def get_url():
    #     return '/relative/path/'

    # full_url = blocks.CharBlock(required=False, default=get_url(), help_text=(
    #         'Copy this relative URL to insert anchor links that take the user to this content section.'
    #         )
    #     )


    def clean(self, data):

        def format_id(string):
            words = string.split('_');
            suffix = ''
            if string:
                suffix = '_'
            if 'anchor' in words:
                return slugify(string)
            else:
                return get_unique_id('anchor_' + slugify(string) + suffix)

        data['link_id'] = format_id(data['link_id'])
        data = super(AnchorLink, self).clean(data)
        return data

    class Meta:
        icon = 'link'
        template = '_includes/atoms/anchor-link.html'
        label = 'Anchor link'
