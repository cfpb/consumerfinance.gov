from django.core.management.base import BaseCommand

from college.disclosures.scripts import nat_stats


COMMAND_HELP = """update_pfc_national_stats gets the latest national statistics
 yaml file from collegescorecard, parses it and updates our local json file at
 college/fixtures/national_stats.json.
"""


class Command(BaseCommand):
    help = COMMAND_HELP

    def handle(self, *args, **options):
        msg = nat_stats.update_national_stats_file()
        self.stdout.write(msg)
