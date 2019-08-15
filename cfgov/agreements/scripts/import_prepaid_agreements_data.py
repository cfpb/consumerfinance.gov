from __future__ import unicode_literals

import datetime

import requests

from agreements.models import PrepaidAgreement, PrepaidProduct


METADATA_SOURCE = 'https://files.consumerfinance.gov/a/assets/prepaid-agreements/prepaid_metadata.json'


def import_products_data(products_data):
    for item in products_data:
        pk = item['product_id'].replace('PRODUCT-', '')
        product = PrepaidProduct.objects.filter(pk=pk).first()
        if not product:
            product = PrepaidProduct(pk=pk)

        withdrawal_date = item['withdrawal_date']
        if withdrawal_date:
            withdrawal_date = datetime.datetime.strptime(
                withdrawal_date, "%m/%d/%Y").date()

        product.name = item['product_name']
        product.issuer_name = item['issuer_name']
        product.prepaid_type = item['prepaid_type']
        product.program_manager = item['program_manager']
        product.other_relevant_parties = item['other_relevant_parties']
        product.status = item['status']
        product.withdrawal_date = withdrawal_date
        product.save()


def import_agreements_data(agreements_data):
    for item in agreements_data:
        pk = item['agreement_id'].replace('IFL-', '')
        agreement = PrepaidAgreement.objects.filter(pk=pk).first()
        if not agreement:
            agreement = PrepaidAgreement(pk=pk)

        effective_date = item['effective_date']
        if effective_date and effective_date != 'None':
            effective_date = datetime.datetime.strptime(
                effective_date, "%m/%d/%Y").date()
        else:
            effective_date = None

        product_id = item['product_id'].replace('PRODUCT-', '')
        product = PrepaidProduct.objects.get(pk=product_id)

        agreement.product = product
        agreement.effective_date = effective_date
        agreement.agreements_files_location = item['agreements_files_location']
        agreement.save()


def run(*args):
    resp = requests.get(url=METADATA_SOURCE)
    data = resp.json()
    import_products_data(data['product'])
    import_agreements_data(data['agreement'])
