from django.test import TestCase

from prepaid_agreements.models import PrepaidProduct
from prepaid_agreements.views import get_available_filters, search_products


class TestViews(TestCase):

    def test_get_available_filters(self):
    	product1 = PrepaidProduct(issuer_name='Bank of CFPB', prepaid_type='Tax')
    	product1.save()
    	product2 = PrepaidProduct(prepaid_type='Travel')
    	product2.save()
    	products = PrepaidProduct.objects.all()
    	self.assertEqual(
    		get_available_filters(products),
    		{'prepaid_type': ['Tax', 'Travel'], 'status': [], 'issuer_name': ['Bank of CFPB']}
    	)

    # def test_search_products_issuer_name(self):
    # 	product1 = PrepaidProduct(issuer_name='Bank of CFPB', prepaid_type='Tax')
    # 	product1.save()
    # 	product2 = PrepaidProduct(prepaid_type='Travel')
    # 	product2.save()
    # 	results = search_products(
    # 		search_term='CFPB',
    # 		search_field=['issuer_name'],
    # 		products=PrepaidProduct.objects.all()
    # 	)
    # 	self.assertEqual(results.first(), product1)
    # 	self.assertCount(results, 1)

    # def test_search_products_all_fields(self):
    # 	product1 = PrepaidProduct(issuer_name='Active Bank')
    # 	product1.save()
    # 	product2 = PrepaidProduct(status='Active')
    # 	product2.save()
    # 	product3 = PrepaidProduct(status='Withdrawn')
    # 	results = search_products(
    # 		search_term='Active',
    # 		search_field=[],
    # 		products=PrepaidProduct.objects.all()
    # 	)
    # 	self.assertIn(results, product1)
    # 	self.assertIn(results, product2)
    # 	self.assertCount(results, 2)
