from django import forms

from .models import ConferenceRegistration


class ConferenceRegistrationForm(forms.ModelForm):
    class Meta:
        model = ConferenceRegistration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ConferenceRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['sessions'].required = True
        self.fields['code'].required = True
        self.fields['sessions'].error_messages.update({
            'required': 'You must select at least one session to attend.'
        })
