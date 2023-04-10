from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

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
            "email": "george@washington.com",
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
    def test_successful_login_object_dne(self):
        """Clear password history and then successfully login"""
        User.objects.get(
            username="admin"
        ).passwordhistoryitem_set.all().delete()
        form = LoginForm(data={"username": "admin", "password": "admin"})
        self.assertTrue(form.is_valid())

    def test_password_expired(self):
        """Ensure login is denied if our password is expired"""
        user = User.objects.get(username="admin")
        PasswordHistoryItem(
            user=user,
            expires_at=now(),
            locked_until=(now() + timedelta(hours=1)),
            encrypted_password=make_password("admin"),
        ).save()

        form = LoginForm(data={"username": "admin", "password": "admin"})
        self.assertFalse(form.is_valid())
        self.assertIn("password has expired", form.errors["__all__"][0])

        # Ensure that a password expiration doesn't result in a failed login
        user.refresh_from_db()
        self.assertFalse(hasattr(user, "failedloginattempt"))
