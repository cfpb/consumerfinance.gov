from django import forms
from django.utils.functional import cached_property

from core.govdelivery import get_govdelivery_api
from data_research.models import ConferenceRegistration


# Form input attributes for Design System compatibility.
#
# See https://cfpb.github.io/design-system/components/text-inputs
# for documentation on the styles that are being duplicated here.
text_input_attrs = {
    'class': 'a-text-input a-text-input__full',
}

# This is needed to disable Django's default Textarea sizing.
textarea_attrs = {
    'rows': None,
    'cols': None,
}
textarea_attrs.update(text_input_attrs)


class ConferenceRegistrationForm(forms.Form):
    """Form for registering an attendee to a conference.

    Creates a ConferenceRegistration model instance upon successful
    registration, and also subscribes the registrant to a GovDelivery
    mailing list.

    If save(commit=False) is used, a model instance is created but not
    persisted to the database, and GovDelivery subscription is skipped.
    """
    ATTENDEE_IN_PERSON = ConferenceRegistration.IN_PERSON
    ATTENDEE_VIRTUALLY = ConferenceRegistration.VIRTUAL
    ATTENDEE_TYPES = tuple((t, t) for t in (
        ATTENDEE_IN_PERSON,
        ATTENDEE_VIRTUALLY,
    ))

    SESSIONS = tuple((s, s) for s in (
        'Thursday morning',
        'Thursday lunch',
        'Thursday afternoon',
        'Friday morning',
    ))

    DIETARY_RESTRICTIONS = tuple((dr, dr) for dr in (
        'Gluten Free',
        'Vegan',
        'Vegetarian',
    ))

    ACCOMMODATIONS = tuple((a, a) for a in (
        'Accessible Seating',
        'ASL Interpreter',
        'Assistive Listening Device',
        'Large Print Materials',
        'Nursing Space',
    ))

    attendee_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=ATTENDEE_TYPES,
        required=True,
        label='Do you plan to attend in person or virtually?',
    )
    name = forms.CharField(
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs=text_input_attrs)
    )
    organization = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs)
    )
    email = forms.EmailField(
        max_length=250,
        required=True,
        widget=forms.EmailInput(attrs=text_input_attrs)
    )
    # sessions = forms.MultipleChoiceField(
    #     widget=CheckboxSelectMultiple,
    #     choices=SESSIONS,
    #     label="Which sessions will you be attending?",
    #     error_messages={
    #         'required': "You must select at least one session to attend.",
    #     }
    # )
    dietary_restrictions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=DIETARY_RESTRICTIONS,
        required=False,
        label="Please let us know about any food allergies or restrictions."
    )
    other_dietary_restrictions = forms.CharField(
        widget=forms.Textarea(attrs=textarea_attrs),
        required=False,
        label="Any other food allergies or restrictions?"
    )
    accommodations = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ACCOMMODATIONS,
        required=False,
        label=(
            "Please let us know of any accommodations you "
            "need in order to attend."
        )
    )
    other_accommodations = forms.CharField(
        widget=forms.Textarea(attrs=textarea_attrs),
        required=False,
        label="Any other accommodations needed to attend?"
    )

    def __init__(self, *args, **kwargs):
        self.capacity = kwargs.pop('capacity')
        self.govdelivery_code = kwargs.pop('govdelivery_code')
        self.govdelivery_question_id = kwargs.pop('govdelivery_question_id')
        self.govdelivery_answer_id = kwargs.pop('govdelivery_answer_id')
        super(ConferenceRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ConferenceRegistrationForm, self).clean()

        if (
            cleaned_data.get('attendee_type') == self.ATTENDEE_IN_PERSON and
            self.at_capacity
        ):
            raise forms.ValidationError('at capacity')

    @property
    def at_capacity(self):
        attendees = ConferenceRegistration.objects.filter(
            govdelivery_code=self.govdelivery_code
        )

        return len(list(attendees.in_person())) >= self.capacity

    def save(self, commit=True):
        registration = ConferenceRegistration(
            govdelivery_code=self.govdelivery_code
        )

        details = dict(self.cleaned_data)
        email = details['email']

        registration.details = details

        if commit:
            # Subscribe this registrant to GovDelivery.
            self.govdelivery_subscribe(code=self.govdelivery_code, email=email)

            # Update their question response, if appropriate.
            if self.govdelivery_question_id and self.govdelivery_answer_id:
                self.govdelivery_question_response(
                    email=email,
                    question_id=self.govdelivery_question_id,
                    answer_id=self.govdelivery_answer_id
                )

            # Persist the registration to the database.
            registration.save()

        return registration

    @cached_property
    def govdelivery_api(self):
        return get_govdelivery_api()

    def govdelivery_subscribe(self, email, code):
        subscription_response = self.govdelivery_api.set_subscriber_topics(
            contact_details=email,
            topic_codes=[code],
            send_notifications=True
        )

        subscription_response.raise_for_status()

    def govdelivery_question_response(self, email, question_id, answer_id):
        question_response = (
            self.govdelivery_api.set_subscriber_answer_to_select_question(
                contact_details=email,
                question_id=question_id,
                answer_id=answer_id
            )
        )

        question_response.raise_for_status()
