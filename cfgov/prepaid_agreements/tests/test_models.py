from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone

from prepaid_agreements.models import PrepaidAgreement, PrepaidProduct


class TestPrepaidProducts(TestCase):

    def test_valid_products(self):
        product1 = PrepaidProduct.objects.create()
        product2 = PrepaidProduct.objects.create(deleted_at=timezone.now())
        valid_products = PrepaidProduct.objects.valid()
        self.assertIn(product1, valid_products)
        self.assertNotIn(product2, valid_products)


class TestMostRecentAgreement(TestCase):
    """ Test that the latest agreement is based on its created date.

    A product can have multiple agreements with the same effective date,
    but the most recent one is considered the one created last.

    An individual agreement is considered most recent if it was
    created last among its product's agreements.
    """

    def setUp(self):
        self.product = PrepaidProduct()
        self.product.save()

        effective_date = date(month=2, day=3, year=2019)
        self.agreement_old = PrepaidAgreement(
            effective_date=effective_date,
            created_time=timezone.now() - timedelta(hours=1),
            product=self.product,
        )
        self.agreement_old.save()
        self.agreement_older = PrepaidAgreement(
            effective_date=effective_date,
            created_time=timezone.now() - timedelta(hours=2),
            product=self.product,
        )
        self.agreement_older.save()
        self.agreement_new = PrepaidAgreement(
            effective_date=effective_date,
            created_time=timezone.now(),
            product=self.product,
        )
        self.agreement_new.save()

    def test_product_most_recent_agreement(self):
        self.assertEqual(
            self.product.most_recent_agreement,
            self.agreement_new
        )

    def test_agreement_is_most_recent(self):
        self.assertEqual(self.agreement_old.is_most_recent, False)
        self.assertEqual(self.agreement_older.is_most_recent, False)
        self.assertEqual(self.agreement_new.is_most_recent, True)
