from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Dump mortgage data to a JSON fixture file"

    def add_arguments(self, parser):
        parser.add_argument("filename", help="Output filename")

    def handle(self, *args, **options):
        # Models to dump, in dependency order
        models = [
            "data_research.MortgageDataConstant",
            "data_research.MortgageMetaData",
            "data_research.State",
            "data_research.MetroArea",
            "data_research.County",
            "data_research.CountyMortgageData",
            "data_research.MSAMortgageData",
            "data_research.StateMortgageData",
            "data_research.NonMSAMortgageData",
            "data_research.NationalMortgageData",
        ]

        # Call dumpdata with the models and write to the specified file
        call_command(
            "dumpdata",
            *models,
            indent=2,
            output=options["filename"],
        )
