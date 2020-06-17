from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from wagtail.core import blocks

from v1.blocks import AbstractFormBlock


class ConferenceRegistrationForm(AbstractFormBlock):
    govdelivery_code = blocks.CharBlock(
        label='GovDelivery code',
        help_text=(
            'Conference registrants will be subscribed to this GovDelivery '
            'topic.'
        )
    )
    govdelivery_question_id = blocks.RegexBlock(
        required=False,
        regex=r'^\d{5,}$',
        error_messages={
            'invalid': 'GovDelivery question ID must be 5 digits.'
        },
        label='GovDelivery question ID',
        help_text=mark_safe(
            'Enter the ID of the question in GovDelivery that is being used '
            'to track registration for this conference. It is the number in '
            'the question URL, e.g., the <code>12345</code> in '
            '<code>https://admin.govdelivery.com/questions/12345/edit</code>.'
        )
    )
    govdelivery_answer_id = blocks.RegexBlock(
        required=False,
        regex=r'^\d{5,}$',
        error_messages={
            'invalid': 'GovDelivery answer ID must be 5 digits.'
        },
        label='GovDelivery answer ID',
        help_text=mark_safe(
            'Enter the ID of the affirmative answer for the above question. '
            'To find it, right-click on the answer in the listing on a page '
            'like <code>https://admin.govdelivery.com/questions/12345/answers'
            '</code>, inspect the element, and look around in the source for '
            'a five-digit ID associated with that answer. <strong>Required '
            'if Govdelivery question ID is set.</strong>'
        )
    )
    capacity = blocks.IntegerBlock(
        help_text=(
            'Enter the (physical) conference attendance limit as a number.'
        )
    )
    success_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown on successful registration.'
        )
    )
    at_capacity_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown when the event is at capacity.'
        )
    )
    failure_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown if the GovDelivery '
            'subscription fails.'
        )
    )

    def clean(self, value):
        cleaned = super(ConferenceRegistrationForm, self).clean(value)
        question = cleaned.get('govdelivery_question_id')
        answer = cleaned.get('govdelivery_answer_id')

        # Question and answer values must both exist or neither exist
        if (question and not answer) or (answer and not question):
            raise ValidationError(
                'Validation error in Conference Registration Form: '
                'GovDelivery question ID requires answer ID, and vice versa.',
                params={'govdelivery_answer_id': ErrorList([
                    'Required if a GovDelivery question ID is entered.'
                ])}
            )

        return cleaned

    class Meta:
        handler = 'data_research.handlers.ConferenceRegistrationHandler'
        template = 'data_research/conference-registration-form.html'


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
