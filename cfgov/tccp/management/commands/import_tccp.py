import argparse

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction

from tccp.dataset import read_survey_data_from_stream
from tccp.models import CardSurveyData
from tccp.utils import get_card_slugifier


class Command(BaseCommand):
    help = "Load TCCP data from Excel spreadsheet."

    def add_arguments(self, parser):
        parser.add_argument(
            "filename",
            type=argparse.FileType("rb"),
            help="Excel spreadsheet containing TCCP data",
        )

    def handle(self, **options):
        slugify_card = get_card_slugifier()

        with transaction.atomic():
            CardSurveyData.objects.all().delete()

            for survey_data in read_survey_data_from_stream(
                options["filename"]
            ):
                card = CardSurveyData(**survey_data)
                card.slug = slugify_card(card)

                try:
                    card.full_clean()
                except ValidationError:
                    self.stderr.write(
                        "Validation failed for card survey data: "
                        f"{survey_data}"
                    )
                    raise

                card.save()
