from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts.notifications import (
    retry_notifications,
)


COMMAND_HELP = (
    "Retry_notifications attempts to resend any notifications "
    "that have failed to reach a school within the past day. "
    "If it succeeds, the notification will be marked as 'sent.'"
    "You can increase the number of days back to look by passing "
    "'--days [NUMBER OF DAYS]' to the command."
)
PARSER_HELP = (
    "This command queries the database for notifications with "
    "a 'sent' value of False. The default time period is one day, "
    "but you can pass a different number of days as an optional '--days' "
    "parameter."
)


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("--days", help=PARSER_HELP, type=int, default=1)

    def handle(self, *args, **options):
        msg = retry_notifications(days=options["days"])
        self.stdout.write(msg)
