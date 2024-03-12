import argparse

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from tccp.models import CardSurveyData


def patch_cards(big_institutions):
    for big_institution in big_institutions:
        cards = CardSurveyData.objects.filter(
            institution_name__exact=big_institution
        )

        if not cards.exists():
            raise CommandError(
                f"No cards found for institution {big_institution}"
            )

        for card in cards:
            card.top_25_institution = True

        CardSurveyData.objects.bulk_update(cards, ["top_25_institution"])


class Command(BaseCommand):
    help = "Patch TCCP data with institution size."

    def add_arguments(self, parser):
        parser.add_argument(
            "filename",
            type=argparse.FileType("r"),
            help="Excel file containing list of top 25 institutions",
        )

    def handle(self, **options):
        big_institutions = [
            line.strip() for line in options["filename"].readlines()
        ]

        with transaction.atomic():
            patch_cards(big_institutions)
