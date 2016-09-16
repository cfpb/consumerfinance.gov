from django import forms
from .models import ConferenceRegistration

class ConferenceRegistrationForm(forms.ModelForm):
    class Meta:
        model = ConferenceRegistration
        fields = '__all__'
