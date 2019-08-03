from __future__ import unicode_literals

import datetime
import json
import os

from agreements.models import PrepaidAgreement, PrepaidProduct


module_dir = os.path.dirname(__file__)


def import_products_data(products_data):
    for item in products_data:
        pk = item['product_id'].replace('PRODUCT-', '')
        product = PrepaidProduct.objects.filter(pk=pk).first()
        if product:
            continue

        withdrawal_date = item['withdrawal_date']
        if withdrawal_date:
            withdrawal_date = datetime.datetime.strptime(
                withdrawal_date, "%d/%m/%Y").date()

        product = PrepaidProduct(
            pk=pk,
            name=item['product_name'],
            issuer_name=item['issuer_name'],
            prepaid_type=item['prepaid_type'],
            program_manager=item['program_manager'],
            other_relevant_parties=item['other_relevant_parties'],
            status=item['status'],
            withdrawal_date=withdrawal_date,
        )
        product.save()


def import_agreements_data(agreements_data):
    for item in agreements_data:
        pk = item['agreement_id'].replace('IFL-', '')
        agreement = PrepaidAgreement.objects.filter(pk=pk).first()
        if agreement:
            continue

        effective_date = item['effective_date']
        if effective_date:
            effective_date = datetime.datetime.strptime(
                effective_date, "%d/%m/%Y").date()

        product_id = item['product_id'].replace('PRODUCT-', '')
        product = PrepaidProduct.objects.get(pk=product_id)

        agreement = PrepaidAgreement(
            pk=pk,
            product=product,
            effective_date=effective_date,
            agreements_files_location=item['agreements_files_location'],
        )
        agreement.save()


def run(*args):
    with open(os.path.join(module_dir, 'products.json')) as products:
        import_products_data(json.load(products))
    with open(os.path.join(module_dir, 'agreements.json')) as agreements:
        import_agreements_data(json.load(agreements))
