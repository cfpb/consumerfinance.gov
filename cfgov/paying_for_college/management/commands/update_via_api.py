from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts import update_colleges


COMMAND_HELP = """update_via_api gets school-level data from the Department of \
Education's CollegeScorecard API. The script intentionally runs slowly \
to avoid triggering API rate limits, so allow an hour to run."""
PARSER_HELP = """Optionally specify a single school to update \
by passing '--school_id' and a college IPEDS ID."""
ID_ERROR = "School could not be found for ID {}"


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument('--school_id', help=PARSER_HELP, default=False)

    def handle(self, *args, **options):
        try:
            (no_data, endmsg) = update_colleges.update(
                single_school=options['school_id'])
        except(IndexError):
            self.stdout.write(ID_ERROR.format(options['school_id']))
        else:
            self.stdout.write(endmsg)
