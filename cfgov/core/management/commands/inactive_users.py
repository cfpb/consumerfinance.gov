from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core import mail
from django.db.models import Q
from django.utils import timezone
from django.utils.formats import date_format


class Command(BaseCommand):
    help = 'Find users who have been inactive for a given amount of time'

    def add_arguments(self, parser):
        parser.add_argument(
            '--period',
            type=int,
            default=90,
            help='The number of days that defines inactivity'
        )
        parser.add_argument(
            '--emails',
            nargs='+',
            default=[],
            help='Email output to a list of addresses'
        )

    def handle(self, *args, **options):
        period = options['period']
        emails = options['emails']

        last_possible_date = timezone.now() - timedelta(days=period)

        User = get_user_model()
        inactive_users = User.objects.filter(
            Q(last_login__lt=last_possible_date) | Q(last_login__isnull=True),
            is_active=True,
            date_joined__lt=last_possible_date
        )

        if len(inactive_users) == 0:
            return

        self.stdout.write('Users inactive for {}+ days:\n'.format(period))
        self.stdout.write(self.format_inactive_users(inactive_users))

        if len(emails) > 0:
            self.stdout.write('Sending inactive user list to '
                              '{}\n'.format(','.join(emails)))
            self.send_email(emails, period, inactive_users)

    def format_inactive_users(self, inactive_users):
        inactive_users_str = ''
        for user in inactive_users:
            if user.last_login is not None:
                last_login = date_format(user.last_login,
                                         "SHORT_DATETIME_FORMAT")
            else:
                last_login = 'never'

            inactive_users_str += '\t{username}: {last_login}\n'.format(
                username=user.username, last_login=last_login)

        return inactive_users_str

    def send_email(self, emails, period, inactive_users):
        now = date_format(timezone.now(), "SHORT_DATETIME_FORMAT")
        subject = 'Inactive users as of {}'.format(now)
        msg = ('The following active users have not logged in for '
               '{period}+ days:\n'.format(period=period))
        msg += self.format_inactive_users(inactive_users)
        email_message = mail.EmailMessage(subject, msg, None, emails)
        email_message.send()
