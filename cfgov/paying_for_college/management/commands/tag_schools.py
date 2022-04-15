from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts import tag_settlement_schools


COMMAND_HELP = """
`tag_schools` updates the 'settlement_school' flag, which is used to mark
 schools that are participating in the disclosure program pursuant
 to a legal settlement. The command accepts one argument, an S3 URL, which
 should point to a CSV of schools subject to settlement. The CSV must contain
 columns for 'ipeds_unit_id' and 'flag'.
"""


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        msg = tag_settlement_schools.tag_schools(options["url"])
        self.stdout.write(msg)
