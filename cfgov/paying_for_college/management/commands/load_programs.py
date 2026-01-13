from django.core.management.base import BaseCommand

from paying_for_college.disclosures.scripts import load_programs


COMMAND_HELP = """update_programs will revise program data based on a CSV
provided by schools. The 'source' argument should be either a CSV file path
or, if the '--s3' option is set, a file name in our validated_data bucket."""
S3_HELP = """Passing '--s3 true' will load a data file from an S3 bucket."""


class Command(BaseCommand):
    help = COMMAND_HELP

    def add_arguments(self, parser):
        parser.add_argument("source", type=str)
        parser.add_argument("--s3", help=S3_HELP, type=str, default="false")

    def handle(self, *args, **options):
        S3 = options["s3"].upper() == "TRUE"
        filesource = options["source"]
        try:
            if S3:
                (FAILED, endmsg) = load_programs.load(filesource, s3=S3)
            else:
                (FAILED, endmsg) = load_programs.load(filesource)
        except Exception as e:
            self.stdout.write(f"Error with script: {e}")
        else:
            if FAILED:
                for fail_msg in FAILED:
                    self.stdout.write(fail_msg)
            self.stdout.write(endmsg)
