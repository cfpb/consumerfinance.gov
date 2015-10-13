from django import forms


class CalenderPDFFilterForm(forms.Form):
    filter_calendar = forms.CharField()
    filter_range_date_gte = forms.DateField(input_formats=['%Y-%m-%d'])
    filter_range_date_lte = forms.DateField(input_formats=['%Y-%m-%d'])

    def clean_filter_calendar(self):
        return self.cleaned_data['filter_calendar'].replace(' ', '+')
