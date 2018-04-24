from django import forms


# Placeholder widget
class RegDownTextarea(forms.Textarea):
    pass


# Placeholder field
class RegDownField(forms.CharField):
    widget = RegDownTextarea
