from wagtail.wagtailcore import blocks

from v1.atomic_elements import atoms, organisms
from v1.blocks import AbstractFormBlock


class ConferenceRegistrationForm(AbstractFormBlock):
    heading = blocks.CharBlock(required=False, help_text=(
        'Note: Non-customizable fields will show up in '
        'Preview and Publish modes.'
    ))
    codes = blocks.ListBlock(blocks.CharBlock(label='Code'), label='GovDelivery codes')
    sessions = blocks.ListBlock(blocks.CharBlock(label='Session'), label='Sessions attending')
    capacity = atoms.IntegerBlock(help_text='Enter an integer that will be the conference attendance limit.')
    at_capacity_message = organisms.FullWidthText(help_text='Enter a message that will be shown when the event is at capacity')

    class Meta:
        handler = 'data_research.handlers.ConferenceRegistrationHandler'
        template = '_includes/conference-registration-form.html'
