import os
import urllib
from datetime import datetime

from django.core.management.base import BaseCommand

from .util import clear_tables, update_agreement, update_issuer, upload_to_s3


class Command(BaseCommand):
    """
    imports credit card agreement data from provided csv
    """

    help = "Upload agreements data from new Quarterly Agreement file path"

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', action='store', required=True)

    def handle(self, *args, **options):
        verbosity = options['verbosity']

        now = datetime.now()
        suffix = '%s_%s_' % (now.month, now.year)

        uri_hostname = 'http://files.consumerfinance.gov'
        s3_key = '/a/assets/credit-card-agreements/pdf'

        clear_tables()

        for current_dir, subdirList, fileList in os.walk(options['path'],
                                                         topdown=True):
            dir_name = os.path.basename(current_dir)

            if ('Credit Card Agreements' in dir_name or
                    'credit_agreements' in dir_name):
                continue
            issuer = update_issuer(dir_name)

            # removes hidden files
            files = [f for f in fileList if not f[0] == '.']
            for fname in files:
                # Make the filename S3-safe by urlencoding it
                unique_fname = suffix + urllib.quote(fname, ' -')

                update_agreement(
                    issuer=issuer, file_name=fname, file_path=os.path.join(
                        current_dir, fname), s3_location=(
                        "%s%s/%s" %
                        (uri_hostname, s3_key, unique_fname)))

                if os.environ.get('AGREEMENTS_S3_UPLOAD_ENABLED', False):
                    file_path = os.path.join(current_dir, fname)
                    s3_dest_path = "%s/%s" % (s3_key, unique_fname)
                    upload_to_s3(file_path, s3_dest_path)

                    if verbosity >= 1:
                        self.stdout.write('{} uploaded to {}'.format(
                            file_path,
                            s3_dest_path
                        ))
