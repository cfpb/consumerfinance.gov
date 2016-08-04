from django.contrib.auth.models import User
from mock import patch
from unittest import TestCase

from v1.auth_forms import UserCreationForm


@patch('v1.auth_forms.send_password_reset_email')
class UserCreationFormTestCase(TestCase):
    def setUp(self):
        self.username = self.__class__.__name__
        self.email = 'george@example.com'

        self.userdata = {
            'email': self.email,
            'username': self.username,
            'first_name': 'George',
            'last_name': 'Washington',
            'password1': 'cherrytree',
            'password2': 'cherrytree',
        }

    def tearDown(self):
        User.objects.filter(username=self.username).delete()

    def test_save_sends_email(self, send_email):
        form = UserCreationForm(self.userdata)
        self.assertTrue(form.is_valid())
        form.save(commit=True)
        send_email.assert_called_once_with(self.email)

    def test_save_without_commit_doesnt_send_email(self, send_email):
        form = UserCreationForm(self.userdata)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        send_email.assert_not_called()
