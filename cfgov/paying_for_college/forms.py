from django import forms

from paying_for_college.validators import validate_uuid4


class FeedbackForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class EmailForm(forms.Form):
    id = forms.CharField(validators=[validate_uuid4])
    email = forms.EmailField()
