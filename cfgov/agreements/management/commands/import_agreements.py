import os
from zipfile import ZipFile

from django.core.management.base import BaseCommand, CommandError

from agreements.management.commands import _util
from agreements.models import Agreement, Issuer


def empty_folder_test(zipfile, pdf_list):
    """Check that there are no empty folders in the agreement zip file."""
    all_folders = set(
        [name for name in zipfile.namelist()
         if name.endswith('/')]
    )
    pdf_folders = set(
        [pdf.split('/')[0] + '/' for pdf in pdf_list]
    )
    empty_folders = all_folders - pdf_folders
    if empty_folders:
        return list(empty_folders)


class Command(BaseCommand):
    """
    imports credit card agreement data from provided zip file.
    """

    help = "Upload agreements data from new Quarterly Agreement "\
           "zip file at --path"

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', action='store', required=True,
                            help="path to a zip file")
        parser.add_argument(
            '--windows',
            action='store_true',
            help='Will process a zip file created via Windows, assuming '
                 'windows-1252 encoding.'
        )

    def handle(self, *args, **options):
        # maybe this should be replaced with a CLI options:
        do_upload = os.environ.get('AGREEMENTS_S3_UPLOAD_ENABLED', False)

        Agreement.objects.all().delete()
        Issuer.objects.all().delete()

        agreements_zip = ZipFile(options['path'])

        all_pdfs = [name for name in agreements_zip.namelist()
                    if name.upper().endswith('.PDF')]
        blanks = empty_folder_test(agreements_zip, all_pdfs)
        if blanks:
            error_msg = (
                "Processing error: Blank folders were found "
                "in the source zip file:\n{}".format(
                    ", ".join([folder for folder in blanks]))
            )
            raise CommandError(error_msg)

        if options['verbosity'] >= 1:
            output_file = self.stdout
        else:
            output_file = open(os.devnull, 'a')

        for pdf_path in all_pdfs:
            _util.save_agreement(
                agreements_zip,
                pdf_path,
                output_file,
                windows=options['windows'],
                upload=do_upload)
