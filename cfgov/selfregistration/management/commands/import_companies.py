import csv
from datetime import datetime
from optparse import make_option
import os.path
import os
import glob

from django.core.management.base import BaseCommand, CommandError

from selfregistration.models import CompanyInfo

class Command(BaseCommand):
    args = '<file ...>'
    help = 'import one or more CSV files, and optionally delete them'

    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete CSV files after a successful export'),
        )
    def handle(self, *csv_paths , **options):
        for path in csv_paths:
            with file(path) as current_file:
                rows = csv.DictReader(current_file)
                for row in rows:
                    company= CompanyInfo(**row)
                    company.save()
                    self.stdout.write("loaded %s\n" % company.company_name)

        if options['delete']:
            for path in csv_paths:
                os.unlink(path)
                self.stdout.write("deleted %s !\n" % path)
