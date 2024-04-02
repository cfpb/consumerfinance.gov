from django.test import TestCase

from tccp.filters import CardOrderingFilter
from tccp.models import CardSurveyData

from .baker import baker


class CardOrderingFilterTests(TestCase):
    def get_queryset(self):
        return CardSurveyData.objects.with_ratings()

    def test_ordering_by_purchase_apr(self):
        for apr in [2.9, 0.9, 99.9, 0]:
            baker.make(
                CardSurveyData,
                targeted_credit_tiers=["Credit score 619 or less"],
                purchase_apr_poor=apr,
            )

        qs = self.get_queryset().for_credit_tier("Credit score 619 or less")
        self.assertQuerysetEqual(
            CardOrderingFilter()
            .filter(qs, ["purchase_apr"])
            .values_list("purchase_apr_for_tier_max", flat=True),
            [0, 0.9, 2.9, 99.9],
        )

    def test_ordering_by_transfer_apr(self):
        for transfer_apr, purchase_apr in [
            (0.2, 0.2),
            (0.1, 0.2),
            (0.1, 0.1),
            (None, 0.3),
        ]:
            baker.make(
                CardSurveyData,
                targeted_credit_tiers=["Credit score 619 or less"],
                purchase_apr_poor=purchase_apr,
                transfer_apr_poor=transfer_apr,
            )

        qs = self.get_queryset().for_credit_tier("Credit score 619 or less")
        self.assertQuerysetEqual(
            CardOrderingFilter()
            .filter(qs, ["transfer_apr"])
            .values_list(
                "transfer_apr_for_tier_max", "purchase_apr_for_tier_max"
            ),
            [(0.1, 0.1), (0.1, 0.2), (0.2, 0.2)],
        )

    def test_ordering_by_product_name(self):
        for product_name in ["e", "a", "b", "d", "c"]:
            baker.make(
                CardSurveyData,
                targeted_credit_tiers=["Credit scores from 620 to 719"],
                product_name=product_name,
            )

        qs = self.get_queryset()
        self.assertQuerysetEqual(
            CardOrderingFilter()
            .filter(qs, ["product_name"])
            .values_list("product_name", flat=True),
            ["a", "b", "c", "d", "e"],
        )
