from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase

from freezegun import freeze_time

from login.forms import LoginForm, UserCreationForm, UserEditForm
from login.models import PasswordHistoryItem


@patch("login.forms.send_password_reset_email")
class UserCreationFormTestCase(TestCase):
    def setUp(self):
        self.username = self.__class__.__name__
        self.email = "george@example.com"

        self.userdata = {
            "email": self.email,
            "username": self.username,
            "first_name": "George",
            "last_name": "Washington",
            "password1": "Cherrytree123&4",
            "password2": "Cherrytree123&4",
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

    def test_duplicate_email_fails_validation(self, send_email):
        User.objects.create(username="foo", email=self.email)
        form = UserCreationForm(self.userdata)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors["email"])


class UserEditFormTestCase(TestCase):
    def setUp(self):
        self.userdata = {
            "username": "george",
            "email": "george@example.com",
            "first_name": "george",
            "last_name": "washington",
        }

    def test_no_edits_valid(self):
        user = User.objects.create(**self.userdata)
        form = UserEditForm(data=self.userdata, instance=user)
        self.assertTrue(form.is_valid())

    def test_edit_first_name(self):
        user = User.objects.create(**self.userdata)

        userdata2 = dict(self.userdata)
        userdata2["first_name"] = "joe"
        form = UserEditForm(data=userdata2, instance=user)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.first_name, "joe")
        self.assertEqual(user.username, "george")

    def test_duplicate_email_fails_validation(self):
        User.objects.create(**self.userdata)

        userdata2 = dict(self.userdata)
        userdata2["username"] = "patrick"
        form = UserEditForm(data=userdata2)

        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors["email"])

    def test_duplicate_emails_allowed_on_user_model(self):
        User.objects.create(**self.userdata)

        userdata2 = dict(self.userdata)
        userdata2["username"] = "patrick"

        try:
            User.objects.create(**userdata2)
        except Exception:
            self.fail(
                "users with duplicate emails are allowed, "
                "just not when creating or editing via for "
            )


class LoginFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="myuser", password="mypass"
        )

    def check_login_with_correct_credentials(self):
        form = LoginForm(data={"username": "myuser", "password": "mypass"})
        self.assertTrue(form.is_valid())

    def test_login_with_correct_credentials(self):
        self.check_login_with_correct_credentials()

    def test_login_successful_if_user_has_no_password_history(self):
        self.user.password_history.all().delete()
        self.check_login_with_correct_credentials()

    def make_login_form_with_expired_password(self):
        self.user.password_history.all().delete()

        with freeze_time("1900-01-01"):
            PasswordHistoryItem.objects.create(
                user=self.user, encrypted_password=make_password("mypass")
            )

        return LoginForm(data={"username": "myuser", "password": "mypass"})

    def test_login_fails_if_user_password_is_too_old(self):
        form = self.make_login_form_with_expired_password()
        self.assertFalse(form.is_valid())
        self.assertIn("Your password has expired", form.errors["__all__"][0])
