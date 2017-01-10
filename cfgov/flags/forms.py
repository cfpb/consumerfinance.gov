from django import forms

from .models import Flag, FlagState


class SelectSiteForm(forms.Form):
    site_id = forms.IntegerField()


class FeatureFlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ('key', )


class FlagStateForm(forms.ModelForm):
    class Meta:
        model = FlagState
        fields = ('flag', 'enabled', 'site')
        widgets = {
            'flag': forms.widgets.HiddenInput(),
            'site': forms.widgets.HiddenInput(),
        }
