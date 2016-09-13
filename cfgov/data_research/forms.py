import django form stuff

class ConferenceRegistrationForm(forms.ModelForm):
    class Meta:
        model = ConferenceRegistration
        fields = '__all__'
        # fields = ['name', 'organization', 'email', 'sessions', 'foodinfo', 'accommodations']

