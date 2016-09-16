from wagtail.wagtailcore import blocks
from v1.blocks import AbstractFormBlock


class ConferenceRegistrationForm(AbstractFormBlock):
    heading = blocks.CharBlock(required=False)
    codes = blocks.ListBlock(blocks.CharBlock(label='Code'), label='GovDelivery codes')
    sessions = blocks.ListBlock(blocks.CharBlock(label='Session'), label='Sessions attending')

    class Meta:
        handler = 'data_research.handlers.ConferenceRegistrationHandler'
        template = 'blocks/conference-registration-form.html'
