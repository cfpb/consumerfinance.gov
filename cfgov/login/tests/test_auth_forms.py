from django.contrib.auth.models import User
from django.test import TestCase

from login.forms import UserCreationForm, UserEditForm


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

    def test_duplicate_email_fails_validation(self):
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
