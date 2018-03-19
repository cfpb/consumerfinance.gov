from __future__ import absolute_import, unicode_literals

from django import forms

from core.govdelivery import get_govdelivery_api
from data_research.models import ConferenceRegistration
from data_research.widgets import (
    CheckboxSelectMultiple, EmailInput, Textarea, TextInput
)


class ConferenceRegistrationForm(forms.Form):
    """Form for registering an attendee to a conference.

    Creates a ConferenceRegistration model instance upon successful
    registration, and also subscribes the registrant to a GovDelivery
    mailing list.

    If save(commit=False) is used, a model instance is created but not
    persisted to the database, and GovDelivery subscription is skipped.
    """
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

    name = forms.CharField(max_length=250, widget=TextInput(required=True))
    organization = forms.CharField(max_length=250, required=False,
                                   widget=TextInput)
    email = forms.EmailField(max_length=250, widget=EmailInput(required=True))
    sessions = forms.MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=SESSIONS,
        label="Which sessions will you be attending?",
        error_messages={
            'required': "You must select at least one session to attend.",
        }
    )
    dietary_restrictions = forms.MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=DIETARY_RESTRICTIONS,
        required=False,
        label="Please let us know about any food allergies or restrictions."
    )
    other_dietary_restrictions = forms.CharField(
        widget=Textarea,
        required=False,
        label="Any other food allergies or restrictions?"
    )
    accommodations = forms.MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=ACCOMMODATIONS,
        required=False,
        label=(
            "Please let us know of any accommodations you "
            "need in order to attend."
        )
    )
    other_accommodations = forms.CharField(
        widget=Textarea,
        required=False,
        label="Any other accommodations needed to attend?"
    )

    def __init__(self, *args, **kwargs):
        self.govdelivery_code = kwargs.pop('govdelivery_code')
        super(ConferenceRegistrationForm, self).__init__(*args, **kwargs)

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

            # Persist the registration to the database.
            registration.save()

        return registration

    def govdelivery_subscribe(self, email, code):
        govdelivery = get_govdelivery_api()
        subscription_response = govdelivery.set_subscriber_topics(
            contact_details=email,
            topic_codes=[code],
            send_notifications=True
        )

        subscription_response.raise_for_status()
