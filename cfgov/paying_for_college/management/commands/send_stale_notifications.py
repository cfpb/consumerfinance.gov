from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts.notifications import (
    send_stale_notifications,
)

COMMAND_HELP = "Send_stale_notifications gathers up stale notifications -- "
"those that are more than a day old and have failed to reach a school -- "
"assembles details and a send log for each notification and emails that "
"to the school and to D&D team members for troubleshooting."
PARSER_HELP = "This command queries the database for notifications with "
"a 'sent' value of False and a timestamp more than a day old. "
"You can pass 'add-email' and a list of emails to send logs to in addition "
"to the school contact."


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument(
            "--add-email", help=PARSER_HELP, nargs="+", type=str
        )

    def handle(self, *args, **options):
        if options["add_email"]:
            msg = send_stale_notifications(add_email=options["add_email"])
        else:
            msg = send_stale_notifications()
        self.stdout.write(msg)
