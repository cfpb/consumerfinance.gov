from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from django.utils.formats import date_format

from wagtail.core.models import PageRevision


User = get_user_model()


def _get_inactive_users(days_back):
    """Find inactive users, by last login and last page edit."""
    pivot_date = timezone.now() - timedelta(days=days_back)
    inactive_users = User.objects.filter(
        Q(last_login__lt=pivot_date) | Q(last_login__isnull=True),
        is_active=True,
        date_joined__lt=pivot_date,
    )
    for user in inactive_users:
        revisions = PageRevision.objects.filter(user=user).order_by(
            "-created_at"
        )
        if revisions and revisions.first().created_at >= pivot_date:
            inactive_users = inactive_users.exclude(pk=user.pk)
    return inactive_users


class Command(BaseCommand):
    help = "Find users who have been inactive for a given amount of time"

    def add_arguments(self, parser):
        parser.add_argument(
            "--period",
            type=int,
            default=90,
            help="Number of days that defines inactivity",
        )
        parser.add_argument(
            "--warn-after",
            type=int,
            default=60,
            help="The number of days prompting an inactivity warning email",
        )
        parser.add_argument(
            "--deactivate-users",
            action="store_true",
            help="A flag to deactivate users over inactivity threshold",
        )
        parser.add_argument(
            "--warn-users",
            action="store_true",
            help="A flag to email inactivity warnings to users",
        )
        parser.add_argument(
            "--emails",
            nargs="+",
            default=[],
            help="Email output to a list of system owner addresses",
        )

    def handle(self, *args, **options):
        period = options["period"]
        emails = options["emails"]
        warn_period = options["warn_after"]

        # Notification flags
        deactivate_users_flag_set = options["deactivate_users"]
        warn_users_flag_set = options["warn_users"]

        inactive_users = _get_inactive_users(period)

        if len(inactive_users) == 0:
            self.stdout.write("No users are inactive {}+ days".format(period))
        else:
            # List inactive users and then deactivate them
            self.stdout.write("Users inactive for {}+ days:\n".format(period))
            self.stdout.write(self.format_inactive_users(inactive_users))

            # Notify specified emails (e.g. system admins)
            if len(emails) > 0:
                self.stdout.write(
                    "Sending inactive user list to "
                    "{}\n".format(",".join(emails))
                )
                self.send_email(emails, period, inactive_users)

            # Deactivate inactive users
            if deactivate_users_flag_set:
                for user in inactive_users:
                    self.deactivate_user(user)
                    self.send_user_deactivation_email(user, period)

                # Deactivate and notify inactive users
                self.stdout.write(
                    "Deactivating and emailing {} users who "
                    "have been inactive for {} days".format(
                        len(inactive_users), period
                    )
                )

        if warn_users_flag_set:
            warn_users = _get_inactive_users(warn_period)

            if len(warn_users) == 0:
                return

            # Notify users approaching deactivation
            self.stdout.write(
                "Emailing {} users who have been "
                "inactive for {} days".format(len(warn_users), warn_period)
            )

            for user in warn_users:
                self.send_user_warning_email(user, warn_period, period)

    def format_inactive_users(self, inactive_users):
        """Formats the list of inactive users for text email"""
        inactive_users_str = ""
        for user in inactive_users:
            if user.last_login is not None:
                last_login = date_format(
                    user.last_login, "SHORT_DATETIME_FORMAT"
                )
            else:
                last_login = "never"

            inactive_users_str += "\t{username}: {last_login}\n".format(
                username=user.username, last_login=last_login
            )

        return inactive_users_str

    def send_email(self, emails, period, inactive_users):
        """Sends a report email to specified emails listing the users who have
        been inactive for the specified time period."""
        now = date_format(timezone.now(), "SHORT_DATETIME_FORMAT")
        subject = "{prefix}Inactive users as of {now}".format(
            prefix=settings.EMAIL_SUBJECT_PREFIX, now=now
        )
        msg = (
            "The following active users have not logged in for "
            "{period}+ days:\n".format(period=period)
        )
        msg += self.format_inactive_users(inactive_users)
        email_message = mail.EmailMessage(subject, msg, None, emails)
        email_message.send()

    def send_user_warning_email(self, user, warn_period, period):
        """Send the specified user a warning that they have been inactive"""
        subject = "{prefix}Wagtail account inactivity".format(
            prefix=settings.EMAIL_SUBJECT_PREFIX
        )
        msg = (
            "Hello,\n\n"
            + "Your consumerfinance.gov Wagtail account has not been "
            + "accessed for more than {} days. In accordance with "
            + "information security policies, if you take no action, your "
            + "account will be deactivated after 90 days of inactivity.\n\n"
            + "To keep your account active, please log in at "
            + "https://content.consumerfinance.gov/admin/\n\n"
            + "Thank you,\nWagtail system owners"
        )
        user.email_user(subject, msg.format(warn_period, period))

    def send_user_deactivation_email(self, user, period):
        """Send the specified user a warning that the have been deactivated
        due to inactivity"""
        subject = "{prefix}Wagtail account deactivation".format(
            prefix=settings.EMAIL_SUBJECT_PREFIX
        )
        msg = (
            "Hello,\n\n"
            + "Your Wagtail account has not been accessed for more than "
            + "{} days. In accordance with information security policies, "
            + "your account has been deactivated.\n\n"
            + "If you require access to Wagtail in the future and would "
            + "like your account to be reactivated, please contact "
            + "Design & Development at designdev@cfpb.gov and indicate your "
            + "business reason for needing access reinstated.\n\n"
            + "Thank you,\nWagtail system owners"
        )
        user.email_user(subject, msg.format(period))

    def deactivate_user(self, user):
        """Deactivate the specified user account"""
        user.is_active = False
        user.save()
