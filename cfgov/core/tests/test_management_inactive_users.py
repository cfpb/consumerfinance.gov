# -*- coding: utf-8 -*-
from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone
from django.utils.formats import date_format

from core.management.commands.inactive_users import Command
from v1.models import LandingPage


class InactiveUsersTestCase(TestCase):
    def setUp(self):
        from v1.models import HomePage

        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.landing_page = LandingPage(title="Landing", slug="landing")
        self.ROOT_PAGE.add_child(instance=self.landing_page)

        User = get_user_model()

        days_91 = timezone.now() - timedelta(days=91)
        days_90 = timezone.now() - timedelta(days=90)
        days_89 = timezone.now() - timedelta(days=89)
        days_61 = timezone.now() - timedelta(days=61)

        # This user is clearly inactive at 91 days
        self.user_1 = User.objects.create(
            username="user_1",
            email="user_1@test.test",
            last_login=days_91,
            date_joined=days_91,
        )

        # This user is inactive because it's the 90th day
        self.user_2 = User.objects.create(
            username="user_2",
            email="user_2@test.test",
            last_login=days_90,
            date_joined=days_91,
        )

        # This user is not inactive because it's been 89 days
        # This user will receive a warning email
        self.user_3 = User.objects.create(
            username="üser_3",
            email="üser_3@test.test",
            last_login=days_89,
            date_joined=days_91,
        )

        # This user has never logged in, joined 91 days ago
        self.user_4 = User.objects.create(
            username="user_4", email="user_4@test.test", date_joined=days_91
        )

        # This user has never logged in, joined today.
        self.user_5 = User.objects.create(
            username="user_5", email="user_5@test.test"
        )

        # This user last logged on 61 days ago, will be warned.
        self.user_6 = User.objects.create(
            username="user_6",
            email="user_6@test.test",
            last_login=days_61,
            date_joined=days_91,
        )

        # This user hasn't logged in for 91 days but has since edited a page.
        self.page_editor = User.objects.create(
            username="page_editor",
            email="page_editor@test.test",
            last_login=days_91,
            date_joined=days_91,
        )
        self.landing_page.save_revision(user=self.page_editor)

        self.stdout = StringIO()

    def get_stdout(self):
        return self.stdout.getvalue()

    def test_format_inactive_users_last_login(self):
        short_date = date_format(
            self.user_1.last_login, "SHORT_DATETIME_FORMAT"
        )
        self.assertEqual(
            Command().format_inactive_users([self.user_1]),
            "\tuser_1: {}\n".format(short_date),
        )

    def test_format_inactive_users_never_logged_in(self):
        self.assertEqual(
            Command().format_inactive_users([self.user_5]), "\tuser_5: never\n"
        )

    def test_get_inactive_users(self):
        """Test that three users are listed for the default 90 period
        including one that last logged in 90 days ago."""
        call_command("inactive_users", stdout=self.stdout)
        self.assertIn("user_1", self.get_stdout())
        self.assertIn("user_2", self.get_stdout())
        self.assertIn("user_4", self.get_stdout())
        self.assertNotIn("üser_3", self.get_stdout())
        self.assertNotIn("user_5", self.get_stdout())
        self.assertNotIn("user_6", self.get_stdout())

    def test_get_inactive_users_87_days(self):
        """Test that four users are listed for a custom 87 day period"""
        call_command("inactive_users", period=87, stdout=self.stdout)
        self.assertIn("user_1", self.get_stdout())
        self.assertIn("user_2", self.get_stdout())
        self.assertIn("üser_3", self.get_stdout())
        self.assertIn("user_4", self.get_stdout())
        self.assertNotIn("user_5", self.get_stdout())
        self.assertNotIn("user_6", self.get_stdout())

    def test_get_inactive_users_92_days(self):
        """Test that no users are listed for a custom 92 day period"""
        call_command("inactive_users", period=92, stdout=self.stdout)
        self.assertNotIn("user_1", self.get_stdout())
        self.assertNotIn("user_2", self.get_stdout())
        self.assertNotIn("üser_3", self.get_stdout())
        self.assertNotIn("user_4", self.get_stdout())
        self.assertNotIn("user_5", self.get_stdout())
        self.assertNotIn("user_6", self.get_stdout())
        self.assertIn("No users are inactive", self.get_stdout())

    @override_settings(EMAIL_SUBJECT_PREFIX="[Prefix]")
    def test_sends_email(self):
        """Test that mail.EmailMessage is called with the appropriate
        list of users"""

        mail.outbox = []
        call_command(
            "inactive_users", emails=["test@example.com"], stdout=self.stdout
        )
        # Outbox will have one system-owner email
        self.assertEqual(len(mail.outbox), 1)

        # Test the first (summary) email for inactive users only
        email = mail.outbox[0]
        self.assertEqual(email.to, ["test@example.com"])
        self.assertEqual(email.from_email, "webmaster@localhost")
        self.assertIn("[Prefix]", email.subject)
        self.assertIn("Inactive users as of", email.subject)

        message = email.message().as_string()
        self.assertIn("user_1", message)
        self.assertIn("user_2", message)
        self.assertIn("user_4", message)
        self.assertNotIn("üser_3", message)
        self.assertNotIn("user_5", message)
        self.assertIn("test@example.com", self.get_stdout())

    def test_sends_email_when_warning(self):
        """Test that mail.EmailMessage is called with the appropriate
        list of users"""

        mail.outbox = []
        call_command("inactive_users", "--warn-users", stdout=self.stdout)
        # Should see 5 warnings since we're not passing `--deactivate`.
        self.assertEqual(len(mail.outbox), 5)

    def test_sends_email_when_deactivating(self):
        """Test that mail.EmailMessage is called with the appropriate
        list of users"""

        mail.outbox = []
        call_command(
            "inactive_users", "--deactivate-users", stdout=self.stdout
        )
        # Outbox will have three inactive user emails
        self.assertEqual(len(mail.outbox), 3)

    def test_sends_email_when_deactivating_and_warning(self):
        """Test that mail.EmailMessage is called with the appropriate
        list of users"""

        mail.outbox = []
        call_command(
            "inactive_users",
            "--deactivate-users",
            "--warn-users",
            stdout=self.stdout,
        )
        # Outbox will have five user emails
        self.assertEqual(len(mail.outbox), 5)

    def test_users_properly_deactivated(self):
        """Test that mail.EmailMessage is called with the appropriate
        list of users"""

        mail.outbox = []
        call_command(
            "inactive_users", "--deactivate-users", stdout=self.stdout
        )

        # Test that users were actually deactivated
        # May need to re-fetch users
        # inactive_users = User.objects.all()
        User = get_user_model()
        self.assertFalse(User.objects.get(username="user_1").is_active)
        self.assertFalse(User.objects.get(username="user_2").is_active)
        self.assertTrue(User.objects.get(username="üser_3").is_active)
        self.assertFalse(User.objects.get(username="user_4").is_active)
        self.assertTrue(User.objects.get(username="user_5").is_active)
        self.assertTrue(User.objects.get(username="user_6").is_active)

    def test_users_properly_deactivated_when_deactivating_and_warning(self):
        """Test that mail.EmailMessage is called with the appropriate
        list of users"""

        mail.outbox = []
        call_command(
            "inactive_users",
            "--deactivate-users",
            "--warn-users",
            stdout=self.stdout,
        )

        # Test that users were actually deactivated
        User = get_user_model()
        self.assertFalse(User.objects.get(username="user_1").is_active)
        self.assertFalse(User.objects.get(username="user_2").is_active)
        self.assertTrue(User.objects.get(username="üser_3").is_active)
        self.assertFalse(User.objects.get(username="user_4").is_active)
        self.assertTrue(User.objects.get(username="user_5").is_active)
        self.assertTrue(User.objects.get(username="user_6").is_active)

        # No warnings if we give the remaining users a save_revision pass.
        mail.outbox = []
        self.landing_page.save_revision(user=self.user_3)
        self.landing_page.save_revision(user=self.user_6)

        call_command("inactive_users", "--warn-users", stdout=self.stdout)
        self.assertEqual(len(mail.outbox), 0)
