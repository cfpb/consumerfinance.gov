from django import forms

from .models import CompanyInfo


class CompanyInfoForm(forms.Form):
    company_name = forms.CharField()
    company_address = forms.CharField()
    company_address2 = forms.CharField(required=False)
    company_city = forms.CharField()
    company_state = forms.CharField()
    company_zip = forms.CharField()
    company_tax_id1 = forms.CharField()
    company_tax_id2 = forms.CharField()
    company_website = forms.CharField(required=False)
    company_phone1 = forms.CharField()
    company_phone2 = forms.CharField()
    company_phone3 = forms.CharField()
    poc_name = forms.CharField()
    poc_title = forms.CharField()
    poc_email = forms.CharField()
    poc_phone1 = forms.CharField()
    poc_phone2 = forms.CharField()
    poc_phone3 = forms.CharField()
    poc_extension = forms.CharField(required=False)
    reg_certify = forms.BooleanField()

    def save(self):
        company_info_data = {}
        form_data = self.cleaned_data

        company_info_data['company_name'] = form_data['company_name']
        company_info_data['address1'] = form_data['company_address']
        company_info_data['address2'] = form_data['company_address2']
        company_info_data['city'] = form_data['company_city']
        company_info_data['state'] = form_data['company_state']
        company_info_data['zip'] = form_data['company_zip']
        company_info_data['tax_id'] = \
            "{company_tax_id1}-{company_tax_id2}".format(**form_data)
        company_info_data['website'] = form_data['company_website']
        company_info_data['company_phone'] = \
            "{company_phone1}-{company_phone2}-{company_phone3}".format(
            **form_data)
        company_info_data['contact_name'] = form_data['poc_name']
        company_info_data['contact_title'] = form_data['poc_title']
        company_info_data['contact_email'] = form_data['poc_email']
        company_info_data['contact_phone'] = \
            "{poc_phone1}-{poc_phone2}-{poc_phone3}".format(
            **form_data)
        company_info_data['contact_ext'] = form_data['poc_extension']

        company = CompanyInfo(**company_info_data)
        company.save()
