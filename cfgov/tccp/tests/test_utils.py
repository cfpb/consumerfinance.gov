from django.test import SimpleTestCase

from tccp.models import CardSurveyData
from tccp.utils import get_card_slugifier


class CardSlugifierTests(SimpleTestCase):
    def test_slugifier(self):
        slugify_card = get_card_slugifier()

        cards = [
            CardSurveyData(
                institution_name=institution_name, product_name=product_name
            )
            for institution_name, product_name in [
                ("Friendly Bank", "SuperCard"),
                ("Another Bank", "Okay Card"),
                ("Another Bank", "Okay Card+"),
                ("Best Bank", "Duplicate Name"),
                ("Best Bank", "Duplicate Name"),
                ("Best Bank", "Duplicate Name"),
            ]
        ]

        self.assertEqual(
            list(map(slugify_card, cards)),
            [
                "friendly-bank-supercard",
                "another-bank-okay-card",
                "another-bank-okay-card-1",
                "best-bank-duplicate-name",
                "best-bank-duplicate-name-1",
                "best-bank-duplicate-name-2",
            ],
        )
