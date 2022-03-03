from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts.update_ipeds import load_values

COMMAND_HELP = """Update_ipeds will download, parse and load the latest
data files from the IPEDS data center. If run without arguments, it will
make a dry run and report how many schools and data points would have been
updated. If run with '--dry-run false' it will update the school records
in the PFC database. The script always fetches the latest academic year
available, which is 2 years behind the calendar year. So in 2016, it fetches
2014 data, which represents data from the 2014-2015 academic year.
"""
PARSER_HELP = """The --dry-run argument defaults to 'true' and makes no
changes to the database. To update the database, pass '--dry-run false'
"""


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", help=PARSER_HELP, type=str, default="true"
        )

    def handle(self, *args, **options):
        if options["dry_run"].lower() == "false":
            msg = load_values(dry_run=False)
        elif options["dry_run"].lower() == "true":
            msg = load_values()
        else:
            msg = PARSER_HELP
        self.stdout.write(msg)
