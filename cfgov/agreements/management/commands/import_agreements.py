import os
from zipfile import ZipFile

import fnmatch

from django.core.management.base import BaseCommand

from agreements.management.commands import util
from agreements.models import Issuer, Agreement


class Command(BaseCommand):
    """
    imports credit card agreement data from provided zip file.
    """

    help = "Upload agreements data from new Quarterly Agreement"\
           "zip file at --path"

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', action='store', required=True,
                            help="path to a zip file")
        parser.add_argument('-e', '--encoding', action='store',
                            default='windows-1252',
                            help="character set used for filenames"
                                 "within the zip file")

    def handle(self, *args, **options):
        source_encoding = options['encoding']
        # maybe this should be replaced with a CLI options:
        do_upload = os.environ.get('AGREEMENTS_S3_UPLOAD_ENABLED', False)

        Agreement.objects.all().delete()
        Issuer.objects.all().delete()

        agreements_zip = ZipFile(options['path'])

        all_pdfs = fnmatch.filter(agreements_zip.namelist(), '*.pdf')

        if options['verbosity'] >= 1:
            output_file = self.stdout
        else:
            output_file = open(os.devnull, 'a')

        for encoded_path in all_pdfs:
            util.save_agreement(agreements_zip, encoded_path,
                                filename_encoding=source_encoding,
                                upload=do_upload,
                                outfile=output_file)
