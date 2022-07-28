import unittest

from django.db import connection
from django.test import TestCase

from prepaid_agreements.models import PrepaidProduct
from prepaid_agreements.views import (
    filter_products,
    get_available_filters,
    search_products,
)


class TestViews(TestCase):
    def setUp(self):
        self.product1 = PrepaidProduct(
            issuer_name="Bank of CFPB",
            prepaid_type="Tax",
            status="Active",
        )
        self.product1.save()
        self.product2 = PrepaidProduct(
            program_manager="CFPB manager",
            prepaid_type="Travel",
            status="Withdrawn",
        )
        self.product2.save()
        self.product3 = PrepaidProduct(
            name="ABC Product",
            issuer_name="ABC Bank",
            prepaid_type="Payroll",
            status="Active",
        )
        self.product3.save()

    def test_get_available_filters(self):
        products = PrepaidProduct.objects
        self.assertEqual(
            get_available_filters(products.none()),
            {"prepaid_type": [], "status": [], "issuer_name": []},
        )
        self.assertEqual(
            get_available_filters(products),
            {
                "prepaid_type": ["Payroll", "Tax", "Travel"],
                "status": ["Active", "Withdrawn"],
                "issuer_name": ["ABC Bank", "Bank of CFPB"],
            },
        )

    @unittest.skipUnless(
        connection.vendor == "postgresql", "PostgreSQL-dependent"
    )
    def test_search_products_issuer_name(self):
        results = search_products(
            search_term="cfpb",
            search_field=["issuer_name"],
            products=PrepaidProduct.objects.all(),
        )
        self.assertIn(self.product1, results)
        self.assertEqual(results.count(), 2)

    @unittest.skipUnless(
        connection.vendor == "postgresql", "PostgreSQL-dependent"
    )
    def test_search_products_all_fields(self):
        results = search_products(
            search_term="cfpb",
            search_field=[],
            products=PrepaidProduct.objects.all(),
        )
        self.assertIn(self.product1, results)
        self.assertIn(self.product2, results)
        self.assertEqual(results.count(), 2)

    def test_filter_products(self):
        results = filter_products(
            filters={
                "status": ["Active"],
                "prepaid_type": ["Travel", "Payroll", "Student"],
                "issuer_name": ["ABC Bank", "XYZ Bank"],
            },
            products=PrepaidProduct.objects.all(),
        )
        self.assertIn(self.product3, results)
        self.assertEqual(results.count(), 1)

    def test_index_search(self):
        response = self.client.get(
            "/data-research/prepaid-accounts/search-agreements/",
            {"q": "cfpb", "search_field": "all", "page": 1},
        )
        self.assertEqual(3, response.context_data["total_count"])
        self.assertEqual(2, response.context_data["current_count"])

    def test_index_filter(self):
        response = self.client.get(
            "/data-research/prepaid-accounts/search-agreements/",
            {"status": "Active"},
        )
        self.assertEqual(3, response.context_data["total_count"])
        self.assertEqual(2, response.context_data["current_count"])
