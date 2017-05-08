# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StringIO import StringIO

from datetime import timedelta

import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone


class InactiveUsersTestCase(TestCase):

    def setUp(self):
        User = get_user_model()

        # This user is clearly inactive at 90 days
        self.user_1 = User.objects.create(username='user_1',
                                          email='user_1@example.com')
        self.user_1.last_login = timezone.now() - timedelta(days=91)
        self.user_1.save()

        # This user is inactive because it's the 90th day
        self.user_2 = User.objects.create(username='user_2',
                                          email='user_2@example.com')
        self.user_2.last_login = timezone.now() - timedelta(days=90)
        self.user_2.save()

        # This user is not inactive because it's been 89 days
        self.user_3 = User.objects.create(username='üser_3',
                                          email='üser_3@example.com')
        self.user_3.last_login = timezone.now() - timedelta(days=89)
        self.user_3.save()

        self.stdout = StringIO()

    def get_stdout(self):
        return self.stdout.getvalue().decode('utf-8')

    def test_get_inactive_users(self):
        """ Test that two users are listed for the default 90 period
        including one that last logged in 90 days ago. """
        call_command('inactive_users', stdout=self.stdout)
        self.assertIn("user_1", self.get_stdout())
        self.assertIn("user_2", self.get_stdout())
        self.assertNotIn("üser_3", self.get_stdout())

    def test_get_inactive_users_87_days(self):
        """ Test that all users are listed for a custom 87 day period """
        out = StringIO()
        call_command('inactive_users', period=87, stdout=self.stdout)
        self.assertIn("user_1", self.get_stdout())
        self.assertIn("user_2", self.get_stdout())
        self.assertIn("üser_3", self.get_stdout())

    def test_get_inactive_users_92_days(self):
        """ Test that no users are listed for a custom 92 day period """
        out = StringIO()
        call_command('inactive_users', period=92, stdout=self.stdout)
        self.assertNotIn("user_1", self.get_stdout())
        self.assertNotIn("user_2", self.get_stdout())
        self.assertNotIn("üser_3", self.get_stdout())

    @mock.patch('core.management.commands.inactive_users.mail.EmailMessage')
    def test_sends_email(self, mock_EmailMessage):
        """ Test that mail.EmailMessage is called with the appropriate
        list of users """
        out = StringIO()
        call_command('inactive_users',
                     emails=['test@example.com'],
                     stdout=self.stdout)
        mock_EmailMessage.return_value.send.assert_called_once()
        message = mock_EmailMessage.call_args[0][1]
        self.assertIn("user_1", message)
        self.assertIn("user_2", message)
        self.assertNotIn("üser_3", message)

        # User list is printed to stdout and a message about sending the
        # email is
        self.assertIn("user_1", self.get_stdout())
        self.assertIn("user_2", self.get_stdout())
        self.assertNotIn("üser_3", self.get_stdout())
        self.assertIn("test@example.com", self.get_stdout() )
