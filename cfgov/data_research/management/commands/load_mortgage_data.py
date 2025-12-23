from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from data_research.models import (
    County,
    CountyMortgageData,
    MetroArea,
    MortgageDataConstant,
    MortgageMetaData,
    MSAMortgageData,
    NationalMortgageData,
    NonMSAMortgageData,
    State,
    StateMortgageData,
)


class Command(BaseCommand):
    help = "Load mortgage data from a JSON fixture file"

    def add_arguments(self, parser):
        parser.add_argument("filename", help="Input filename")

    def handle(self, *args, **options):
        # Models to delete, in reverse dependency order
        models = [
            NationalMortgageData,
            NonMSAMortgageData,
            StateMortgageData,
            MSAMortgageData,
            CountyMortgageData,
            County,
            MetroArea,
            State,
            MortgageMetaData,
            MortgageDataConstant,
        ]

        self.stdout.write("Loading mortgage data...")

        with transaction.atomic():
            self.stdout.write("Deleting existing data...")
            for model in models:
                count = model.objects.count()
                model.objects.all().delete()
                self.stdout.write(
                    f"\tDeleted {count} {model._meta.verbose_name_plural}"
                )

            self.stdout.write("Loading data from file...")
            call_command("loaddata", options["filename"])

        for model in models:
            count = model.objects.count()
            self.stdout.write(
                f"\tLoaded {count} {model._meta.verbose_name_plural}"
            )
