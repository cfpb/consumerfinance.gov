from wagtail.wagtailcore import blocks

from v1.atomic_elements import atoms, organisms
from v1.blocks import AbstractFormBlock


class ConferenceRegistrationForm(AbstractFormBlock):
    heading = blocks.CharBlock(required=False, help_text=(
        'Note: Additional form field options will appear in '
        'Preview and Publish modes.'
    ))
    code = blocks.CharBlock(label='GovDelivery Code')
    sessions = blocks.ListBlock(
        blocks.CharBlock(label='Session'),
        label='Sessions attending'
    )
    capacity = atoms.IntegerBlock(help_text=(
        'Enter an integer that will be the conference attendance limit.'
    ))
    success_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown on successful registration.'
        )
    )
    at_capacity_message = organisms.FullWidthText(
        help_text=(
            'Enter a message that will be shown when the event is at capacity.'
        )
    )
    failure_message = blocks.CharBlock(
        help_text=(
            'Enter a message that will be shown if the GovDelivery '
            'subscription fails.'
        )
    )

    class Meta:
        handler = 'data_research.handlers.ConferenceRegistrationHandler'
        template = '_includes/conference-registration-form.html'


class MortgageDataDownloads(blocks.StructBlock):
    show_archives = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text=(
            'Check this box to allow the archival section to display. '
            'No section will appear if there are no archival downloads.'))

    class Meta:
        label = 'Mortgage Downloads Block'
        icon = 'table'
        template = '_includes/organisms/mortgage-performance-downloads.html'
