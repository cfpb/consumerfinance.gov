import unittest

from django.db import connection
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from prepaid_agreements.models import PrepaidProduct
from prepaid_agreements.views import (
    filter_products, get_available_filters, get_detail_page_breadcrumb,
    search_products
)


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

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
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
        self.assertIn(product1, results)
        self.assertEqual(results.count(), 1)

    @unittest.skipUnless(
        connection.vendor == 'postgresql', 'PostgreSQL-dependent')
    def test_search_products_all_fields(self):
        product1 = PrepaidProduct(issuer_name='XYZ Bank')
        product1.save()
        product2 = PrepaidProduct(program_manager='xyz manager')
        product2.save()
        product3 = PrepaidProduct(name='Foo Bar Product')
        product3.save()
        results = search_products(
            search_term='Xyz',
            search_field=[],
            products=PrepaidProduct.objects.all()
        )
        self.assertIn(product1, results)
        self.assertIn(product2, results)
        self.assertEqual(results.count(), 2)

    def test_filter_products(self):
        product1 = PrepaidProduct(status='Active', prepaid_type='Student')
        product1.save()
        product2 = PrepaidProduct(
            status='Withdrawn', prepaid_type='Travel', issuer_name='XYZ Bank')
        product2.save()
        product3 = PrepaidProduct(
            status='Active', prepaid_type='Payroll', issuer_name='ABC Bank')
        product3.save()
        results = filter_products(
            filters={
                'status': ['Active'],
                'prepaid_type': ['Travel', 'Payroll', 'Student'],
                'issuer_name': ['ABC Bank', 'XYZ Bank']
            },
            products=PrepaidProduct.objects.all()
        )
        self.assertIn(product3, results)
        self.assertEqual(results.count(), 1)

    def test_get_breadcrumb_if_referrer_is_search_page_with_query(self):
        request = HttpRequest()
        search_path_with_query = reverse('prepaid_agreements:index') + '?q=a'
        request.META.update({'HTTP_REFERER': search_path_with_query})
        self.assertEqual(
            get_detail_page_breadcrumb(request),
            search_path_with_query
        )

    def test_get_breadcrumb_if_referrer_is_search_page_without_query(self):
        request = HttpRequest()
        search_path = reverse('prepaid_agreements:index')
        request.META.update({'HTTP_REFERER': search_path})
        self.assertEqual(get_detail_page_breadcrumb(request), search_path)

    def test_get_breadcrumb_if_referrer_is_not_search_page(self):
        request = HttpRequest()
        search_path = reverse('prepaid_agreements:index')
        request.META.update({'HTTP_REFERER': '/random-path/'})
        self.assertEqual(get_detail_page_breadcrumb(request), search_path)

    def test_get_breadcrumb_if_referrer_is_random_page_with_query(self):
        request = HttpRequest()
        search_path = reverse('prepaid_agreements:index')
        request.META.update({'HTTP_REFERER': '/random-path/?q=test'})
        self.assertEqual(get_detail_page_breadcrumb(request), search_path)

    def test_get_breadcrumb_if_no_referrer(self):
        request = HttpRequest()
        search_path = reverse('prepaid_agreements:index')
        self.assertEqual(get_detail_page_breadcrumb(request), search_path)
