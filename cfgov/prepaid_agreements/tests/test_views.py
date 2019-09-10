from django.test import TestCase

from prepaid_agreements.models import PrepaidProduct
from prepaid_agreements.views import get_available_filters, search_products


class TestViews(TestCase):

    def test_get_available_filters(self):
        product1 = PrepaidProduct(
            issuer_name='Bank of CFPB',
            prepaid_type='Tax'
        )
        product1.save()
        product2 = PrepaidProduct(prepaid_type='Travel')
        product2.save()
        products = PrepaidProduct.objects.all()
        self.assertEqual(
            get_available_filters(products),
            {
                'prepaid_type': ['Tax', 'Travel'],
                'status': [],
                'issuer_name': ['Bank of CFPB']
            }
        )

    def test_search_products_issuer_name(self):
        product1 = PrepaidProduct(issuer_name='Bank of CFPB')
        product1.save()
        product2 = PrepaidProduct(issuer_name='Bank of Foo Bar')
        product2.save()
        results = search_products(
            search_term='cfpb',
            search_field=['issuer_name'],
            products=PrepaidProduct.objects.all()
        )
        self.assertEqual(results.first(), product1)
        self.assertEqual(results.count(), 1)

    def test_search_products_all_fields(self):
        product1 = PrepaidProduct(issuer_name='Active Bank')
        product1.save()
        product2 = PrepaidProduct(program_manager='active manager')
        product2.save()
        product3 = PrepaidProduct(name='Foo Bar Product')
        product3.save()
        results = search_products(
            search_term='Active',
            search_field=[],
            products=PrepaidProduct.objects.all()
        )
        self.assertIn(product1, results)
        self.assertIn(product2, results)
        self.assertEqual(results.count(), 2)
