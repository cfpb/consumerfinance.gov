from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils.timezone import now

from login.forms import (
    CFGOVPasswordChangeForm,
    LoginForm,
    UserCreationForm,
    UserEditForm,
)
from login.models import (
    FailedLoginAttempt,
    PasswordHistoryItem,
    TemporaryLockout,
)
from login.tests.test_password_policy import TestWithUser


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
            "password1": "cherrytree",
            "password2": "cherrytree",
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


class PasswordValidationMixinTestCase(TestWithUser):
    def test_edit_password(self):
        user = self.get_user(last_password="testing")
        form = CFGOVPasswordChangeForm(
            data={
                "old_password": "testing",
                "new_password1": "Testing12345!",
                "new_password2": "Testing12345!",
            },
            user=user,
        )
        form.is_valid()
        self.assertTrue(form.is_valid())


class LoginFormTestCase(TestCase):
    def test_successful_login(self):
        form = LoginForm(data={"username": "admin", "password": "admin"})
        self.assertTrue(form.is_valid())

    def test_successful_login_object_dne(self):
        """Clear password history and then successfully login"""
        User.objects.get(
            username="admin"
        ).passwordhistoryitem_set.all().delete()
        form = LoginForm(data={"username": "admin", "password": "admin"})
        self.assertTrue(form.is_valid())

    def test_failed_login_recorded(self):
        """Record the failure for a failed login"""
        form = LoginForm(data={"username": "admin", "password": "badadmin"})
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(
            User.objects.get(username="admin").failedloginattempt
        )

    def test_failed_login_invalid_user(self):
        """Handle a non-existent user when a login fails"""
        form = LoginForm(data={"username": "badmin", "password": "badadmin"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "correct username and password", form.errors["__all__"][0]
        )

    @override_settings(LOGIN_FAILS_ALLOWED=0)
    def test_failed_login_lockout(self):
        """Ensure lockout if our failed logins are over our limit"""
        form = LoginForm(data={"username": "admin", "password": "badadmin"})
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError):
            form.check_for_lockout(User.objects.get(username="admin"))

    def test_login_locked_out(self):
        """Ensure we get locked out"""
        form = LoginForm()
        user = User.objects.get(username="admin")
        TemporaryLockout(
            user=user, expires_at=(now() + timedelta(hours=1))
        ).save()
        user.refresh_from_db()
        with self.assertRaises(ValidationError):
            form.check_for_lockout(user)

    def test_password_expired(self):
        """Ensure login is denied if our password is expired"""
        form = LoginForm()
        user = User.objects.get(username="admin")
        PasswordHistoryItem(
            user=user,
            expires_at=now(),
            locked_until=(now() + timedelta(hours=1)),
            encrypted_password=make_password("testing"),
        ).save()
        user.refresh_from_db()
        with self.assertRaises(ValidationError):
            form.check_for_password_expiration(user)

    def test_clear_failed_login_attempts(self):
        """Ensure we can clear failed login attempts"""
        form = LoginForm()
        user = User.objects.get(username="admin")
        FailedLoginAttempt(user=user).save()

        user.refresh_from_db()
        self.assertIsNotNone(user.failedloginattempt)

        form.clear_failed_login_attempts(user)

        user.refresh_from_db()
        with self.assertRaises(
            User.failedloginattempt.RelatedObjectDoesNotExist
        ):
            user.failedloginattempt
