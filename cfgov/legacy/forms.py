from django import forms
from localflavor.us.forms import USZipCodeField


class HousingCounselorForm(forms.Form):
    zip = USZipCodeField()
