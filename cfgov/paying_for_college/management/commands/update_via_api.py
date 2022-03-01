from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts import update_colleges


COMMAND_HELP = """update_via_api gets school-level data from the Department of \
Education's CollegeScorecard API. The script intentionally runs slowly \
to avoid triggering API rate limits, so allow an hour to run."""
PARSER_HELP = """Optionally specify a single school to update \
by passing '--school_id' and a college IPEDS ID."""
PROGRAMS_HELP = """Optionally choose to harvest program-level data \
by passing the '--save_programs' option."""
ID_ERROR = "School could not be found for ID {}"


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("--school_id", help=PARSER_HELP, default=False)
        parser.add_argument("--save_programs", action="store_true", help=PROGRAMS_HELP)

    def handle(self, *args, **options):
        save_programs = options.get("save_programs") or False
        single_school = options.get("school_id")
        if save_programs and single_school:
            (no_data, endmsg) = update_colleges.update(
                single_school=single_school, store_programs=True
            )
        elif single_school:
            (no_data, endmsg) = update_colleges.update(single_school=single_school)
        elif save_programs:
            (no_data, endmsg) = update_colleges.update(store_programs=True)
        else:
            (no_data, endmsg) = update_colleges.update()
        self.stdout.write(endmsg)
