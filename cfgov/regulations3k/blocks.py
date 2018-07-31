from wagtail.wagtailcore import blocks

from v1 import blocks as v1_blocks
from v1.atomic_elements import organisms


class RegulationsList(organisms.ModelBlock):
    model = 'regulations3k.RegulationPage'
    ordering = ('regulation')

    heading = blocks.CharBlock(
        required=False,
        help_text='Regulations list heading'
    )
    more_regs_page = blocks.PageChooserBlock(
        help_text='Link to more regulations'
    )
    more_regs_text = blocks.CharBlock(
        required=False,
        help_text='Text to show on link to more regulations'
    )

    def get_context(self, value, parent_context=None):
        context = super(RegulationsList, self).get_context(
            value, parent_context=parent_context
        )
        context['regulations'] = self.get_queryset(value)
        return context

    class Meta:
        icon = 'list-ul'
        template = 'regulations3k/regulations-listing.html'


class RegulationsFullWidthText(blocks.StreamBlock):
    content = blocks.RichTextBlock(icon='edit')
    regulations_list = RegulationsList()
    reusable_text = v1_blocks.ReusableTextChooserBlock('v1.ReusableText')

    class Meta:
        icon = 'edit'
        template = '_includes/organisms/full-width-text.html'
