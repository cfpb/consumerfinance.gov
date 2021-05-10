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
    """ Test that the latest agreement is based on effective date.

    The most_recent_agreement method on a PrepaidProduct should return the
    agreement with the latest effective_date.

    If multiple agreements exist for a product with the same effective_date,
    return the one with the latest created_time.
    """

    def setUp(self):
        march_1 = date(month=3, day=1, year=2021)
        april_1 = date(month=4, day=1, year=2021)
        now = timezone.now()
        earlier = now - timedelta(hours=1)

        # Agreements with same created_time and different effective_date
        self.product_1 = PrepaidProduct()
        self.product_1.save()
        self.agreement_1 = PrepaidAgreement(
            effective_date=april_1,
            created_time=now,
            product=self.product_1,
        )
        self.agreement_1.save()

        self.effective_earlier = PrepaidAgreement(
            effective_date=march_1,
            created_time=now,
            product=self.product_1,
        )
        self.effective_earlier.save()

        # Agreements with same effective_date and different created_time
        self.product_2 = PrepaidProduct()
        self.product_2.save()
        self.agreement_2 = PrepaidAgreement(
            effective_date=april_1,
            created_time=now,
            product=self.product_2,
        )
        self.agreement_2.save()
        self.created_earlier = PrepaidAgreement(
            effective_date=april_1,
            created_time=earlier,
            product=self.product_2,
        )
        self.created_earlier.save()

    def test_product_most_recent_agreement(self):
        self.assertEqual(
            self.product_1.most_recent_agreement,
            self.agreement_1
        )
        self.assertEqual(
            self.product_2.most_recent_agreement,
            self.agreement_2
        )

    def test_agreement_is_most_recent(self):
        self.assertTrue(self.agreement_1.is_most_recent)
        self.assertTrue(self.agreement_2.is_most_recent)

        self.assertFalse(self.created_earlier.is_most_recent)
        self.assertFalse(self.effective_earlier.is_most_recent)
