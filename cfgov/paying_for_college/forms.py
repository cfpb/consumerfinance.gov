from django import forms


class FeedbackForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
