from django import forms


class HousingCounselorForm(forms.Form):
    zip = forms.IntegerField(label='Zipcode', max_value=99999)
