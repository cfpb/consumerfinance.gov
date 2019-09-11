from __future__ import unicode_literals

from datetime import datetime

import requests
from pytz import timezone

from prepaid_agreements.models import PrepaidAgreement, PrepaidProduct


S3_PATH = 'https://files.consumerfinance.gov/a/assets/prepaid-agreements/'
METADATA_FILENAME = 'prepaid_metadata.json'


def import_products_data(products_data):
    for item in products_data:
        pk = item['product_id'].replace('PRODUCT-', '')
        product = PrepaidProduct.objects.filter(pk=pk).first()
        if not product:
            product = PrepaidProduct(pk=pk)

        withdrawal_date = item['withdrawal_date']
        if withdrawal_date:
            withdrawal_date = datetime.strptime(
                withdrawal_date, "%m/%d/%Y").date()

        product.name = item['product_name']
        product.issuer_name = item['issuer_name']
        product.prepaid_type = item['prepaid_type']
        product.program_manager = item['program_manager']
        product.program_manager_exists = item['program_manager_exists']
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
            effective_date = datetime.strptime(
                effective_date, '%m/%d/%Y').date()
        else:
            effective_date = None

        created_time = datetime.strptime(
            item['created_date'],
            '%Y-%m-%d %H:%M:%S'
        )
        created_time = created_time.replace(tzinfo=timezone('EST'))

        product_id = item['product_id'].replace('PRODUCT-', '')
        product = PrepaidProduct.objects.get(pk=product_id)
        url = S3_PATH + item['agreements_files_location']

        agreement.product = product
        agreement.created_time = created_time
        agreement.effective_date = effective_date
        agreement.compressed_files_url = url
        agreement.bulk_download_path = item['path']
        agreement.filename = item['agreements_files_location']
        agreement.save()


def run(*args):
    source_url = S3_PATH + METADATA_FILENAME
    resp = requests.get(url=source_url)
    data = resp.json()

    import_products_data(data['products'])
    import_agreements_data(data['agreements'])
