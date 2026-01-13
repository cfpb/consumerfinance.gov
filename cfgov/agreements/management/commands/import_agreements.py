import os
import tempfile
import urllib
from contextlib import contextmanager, nullcontext
from pathlib import Path
from zipfile import ZipFile

from django.core.management.base import BaseCommand, CommandError

from agreements.management.commands import _util
from agreements.models import Agreement, Issuer


def validate_contains_pdfs(pdf_list):
    """
    Check that the zip file contains at least one PDF.
    If not, raise a CommandError.
    """
    if len(pdf_list) == 0:
        error_msg = "No PDFs were detected in the input file."
        raise CommandError(error_msg)


def validate_no_empty_folders(zipfile, pdf_list):
    """
    Check that there are no empty folders in the agreement zip file.
    If there are, raise a CommandError.
    """
    all_folders = set(
        [Path(name) for name in zipfile.namelist() if name.endswith("/")]
    )
    pdf_folders = set([Path(pdf_path).parent for pdf_path in pdf_list])

    # Ensure folders at higher levels of the directory structure
    # don't get marked as empty
    sample_pdf = Path(pdf_list[0])
    for p in sample_pdf.parents:
        pdf_folders.add(p)

    empty_folders = all_folders - pdf_folders
    if empty_folders:
        error_msg = (
            "Processing error: Blank folders were found "
            "in the source zip file:\n{}".format(
                ", ".join([str(folder) for folder in empty_folders])
            )
        )
        raise CommandError(error_msg)


@contextmanager
def fetch_agreements_zip(path_or_url):
    """Yield a path to the agreements zip file

    If the path_or_url is a URL, this will download it to a temporary
    file, yield that path, and when the context manager closes, remove
    the temporary file.

    If the path_or_url is just a path, it will be returned as-is, with
    no file management.

    No validation of the file is done here.
    """
    # If it's just a path, return it.
    if urllib.parse.urlparse(path_or_url).scheme == "":
        yield path_or_url
    else:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Bandit will flag this for taking file:// URLs, but in this
            # context, file:// URLs are not necessarily unexpected.
            agreements_zip_path, headers = urllib.request.urlretrieve(
                path_or_url, Path(tmpdirname) / Path("agreements.zip")
            )  # nosec B310
            yield agreements_zip_path


class Command(BaseCommand):
    """
    imports credit card agreement data from provided zip file.
    """

    help = (
        "Upload agreements data from new Quarterly Agreement "
        "zip file at --path"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            action="store",
            required=True,
            help="path or URL to a zip file",
        )
        parser.add_argument(
            "--windows",
            action="store_true",
            help="DEPRECATED. Will process a zip file created via Windows, "
            "assuming windows-1252 encoding.",
        )
        parser.add_argument(
            "--upload-to-s3",
            action="store_true",
            help="Will upload the agreements files to S3 if configured.",
        )

    def handle(self, *args, **options):
        do_upload = options["upload_to_s3"]

        with fetch_agreements_zip(options["path"]) as agreements_zip_path:
            agreements_zip = ZipFile(agreements_zip_path)
            all_pdfs = [
                _util.filename_in_zip(info)
                for info in agreements_zip.infolist()
                if info.filename.upper().endswith(".PDF")
            ]

            validate_contains_pdfs(all_pdfs)
            validate_no_empty_folders(agreements_zip, all_pdfs)

            Agreement.objects.all().delete()
            Issuer.objects.all().delete()

            with (
                nullcontext(self.stdout)
                if options["verbosity"] >= 1
                else open(os.devnull, "a")
            ) as output_file:
                for pdf_path in all_pdfs:
                    _util.save_agreement(
                        agreements_zip, pdf_path, output_file, upload=do_upload
                    )
