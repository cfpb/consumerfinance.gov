"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from selfregistration.forms import CompanyInfoForm


class UserFacingViews(TestCase):
    def setUp(self):

        form_data = {}

        form_data['company_name'] = 'My cool company'
        form_data['company_address'] = "1212 Temporary Street"
        form_data['company_address2'] = "Recieving"
        form_data['company_city'] = "New York"
        form_data['company_state'] = "NY"
        form_data['company_zip'] = '10036'
        form_data['company_tax_id1'] = '11'
        form_data['company_tax_id2'] = '1111111'
        form_data['company_phone1'] = '111'
        form_data['company_phone2'] = '111'
        form_data['company_phone3'] = '1111'
        form_data['poc_name'] = 'Pointo Contact'
        form_data['poc_title'] = 'CFO'
        form_data['poc_email'] = 'noreply@cfpb.gov'
        form_data['poc_phone1'] = '222'
        form_data['poc_phone2'] = '222'
        form_data['poc_phone3'] = '2222'
        form_data['reg_certify'] = True

        self.form_data = form_data

        self.superuser = User.objects.create_superuser(username='superuser',
                                                       email='',
                                                       password='password')

        form = CompanyInfoForm(self.form_data)

        assert(form.is_valid())

        form.save()

    def test_simple_render(self):
        """
        Test that the index page is reachable
        """
        url = reverse('company-signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_valid_submission(self):

        url = reverse('company-signup')
        response = self.client.post(url, self.form_data)
        self.assertEquals(response.status_code, 200)

    def test_export_all(self):
        url = reverse('export_registrations')

        self.client.login(username='superuser', password='password')
        response = self.client.post(url, {'export_all': True})
        self.assertContains(response, 'My cool company')
