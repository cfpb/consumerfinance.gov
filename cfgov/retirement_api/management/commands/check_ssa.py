from django.core.management.base import BaseCommand

from retirement_api.utils import check_api


COMMAND_HELP = """Sends a test post to SSA's Quick Calculator \
and checks the results to make sure we're getting valid results."""
PARSER_HELP = """Specify server to use. default is 'build', \
only current option is 'prod'
"""


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("--server", default="build", help=PARSER_HELP)

    def handle(self, *args, **options):
        result = check_api.run(options["server"])
        self.stdout.write(check_api.build_msg(result))
