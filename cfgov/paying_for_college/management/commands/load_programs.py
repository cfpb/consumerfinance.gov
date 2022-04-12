from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts import load_programs


COMMAND_HELP = """update_programs will update program data based on
a CSV provided by schools.  The source argument should be a CSV file path
or, if the '--s3 true' option is passed, source should be an S3 URL."""
S3_HELP = """Passing '--s3 true' will point the script at S3 intead of
a file system path. The source argument should be an S3 endpoint."""


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("source", nargs="+", type=str)
        parser.add_argument("--s3", help=S3_HELP, type=str, default="false")

    def handle(self, *args, **options):
        if options["s3"].upper() == "TRUE":
            S3 = True
        else:
            S3 = False
        for filesource in options["source"]:
            try:
                if S3:
                    (FAILED, endmsg) = load_programs.load(filesource, s3=S3)
                else:
                    (FAILED, endmsg) = load_programs.load(filesource)
            except Exception:
                self.stdout.write("Error with script")
            else:
                if FAILED:
                    for fail_msg in FAILED:
                        self.stdout.write(fail_msg)
                self.stdout.write(endmsg)
