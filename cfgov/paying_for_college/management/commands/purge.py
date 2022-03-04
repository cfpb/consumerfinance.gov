from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts.purge_objects import purge


COMMAND_HELP = (
    "Purge will wipe out notifications or programs "
    "in the local Django database. "
    "It can't be run against any other models, "
    "and you must provide an object type to purge.\n"
    "Purge all notifications with 'manage.py purge notifications'\n"
    "Purge all projects with 'manage.py purge projects'\n"
    "Purge test projecs with 'manage.py purge test-projects'"
)


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("objects", type=str)

    def handle(self, *args, **options):
        msg = purge(options["objects"])
        self.stdout.write(msg)
