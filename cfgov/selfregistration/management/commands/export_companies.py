import csv
from datetime import datetime
from optparse import make_option
import os.path

from django.core.management.base import BaseCommand

from selfregistration.models import CompanyInfo


class Command(BaseCommand):
    args = '<directory>'
    help = 'Export records to a directory, and delete them'

    option_list = BaseCommand.option_list + (
        make_option('--delete',
                    action='store_true',
                    dest='delete',
                    default=False,
                    help='Delete records after a successful export'),
    )

    def handle(self, output_dir, **options):
        timestamp = datetime.now()
        filename = timestamp.strftime("companies_%Y%m%d%H%M%s.csv")
        output_path = os.path.join(output_dir, filename)
        writer = csv.writer(file(output_path, 'w'))
        all_companies = CompanyInfo.objects.all()
        companies_to_export = all_companies.filter(submitted__lte=timestamp)

        writer.writerow(['company_name',
                         'address1',
                         'address2',
                         'city',
                         'state',
                         'zip',
                         'tax_id',
                         'website',
                         'company_phone',
                         'contact_name',
                         'contact_title',
                         'contact_email',
                         'contact_phone',
                         'contact_ext'])

        for row in companies_to_export:
            writer.writerow([row.company_name,
                             row.address1,
                             row.address2,
                             row.city,
                             row.state,
                             row.zip,
                             row.tax_id,
                             row.website,
                             row.company_phone,
                             row.contact_name,
                             row.contact_title,
                             row.contact_email,
                             row.contact_phone,
                             row.contact_ext])
        self.stdout.write("Exported records to %s\n" % output_path)

        if options['delete']:
            to_delete = all_companies.filter(submitted__lte=timestamp)
            to_delete.delete()

            self.stdout.write("And deleted them!\n")
