from datetime import datetime

from django.utils import timezone

import pytz
import requests

from prepaid_agreements.models import PrepaidAgreement, PrepaidProduct


S3_PATH = "https://files.consumerfinance.gov/a/assets/prepaid-agreements/"
METADATA_FILENAME = "prepaid_metadata.json"


def mark_deleted_products(valid_products):
    PrepaidProduct.objects.exclude(pk__in=valid_products).exclude(
        deleted_at__isnull=False
    ).update(deleted_at=timezone.now())


def import_products_data(products_data):
    imported_products = []
    for item in products_data:
        pk = item["product_id"].replace("PRODUCT-", "")
        imported_products.append(pk)

        withdrawal_date = item["withdrawal_date"]
        if withdrawal_date:
            withdrawal_date = datetime.strptime(
                withdrawal_date, "%m/%d/%Y"
            ).date()

        PrepaidProduct.objects.update_or_create(
            pk=pk,
            defaults={
                "name": item["product_name"],
                "issuer_name": item["issuer_name"],
                "prepaid_type": item["prepaid_type"],
                "program_manager": item["program_manager"],
                "program_manager_exists": item["program_manager_exists"],
                "other_relevant_parties": item["other_relevant_parties"],
                "status": item["status"],
                "withdrawal_date": withdrawal_date,
            },
        )
    return imported_products


def import_agreements_data(agreements_data):
    for item in agreements_data:
        pk = item["agreement_id"].replace("IFL-", "")

        effective_date = item["effective_date"]
        if effective_date and effective_date != "None":
            effective_date = datetime.strptime(
                effective_date, "%m/%d/%Y"
            ).date()
        else:
            effective_date = None

        created_time = datetime.strptime(
            item["created_date"], "%Y-%m-%d %H:%M:%S"
        )
        created_time = created_time.replace(tzinfo=pytz.timezone("EST"))

        product_id = item["product_id"].replace("PRODUCT-", "")
        product = PrepaidProduct.objects.get(pk=product_id)
        url = S3_PATH + item["agreements_files_location"]

        if "_" in product.name:
            bulk_path = item["path"].split("/")[2]
            bulk_download_path = (
                product.issuer_name + "/" + product.name + "/" + bulk_path
            )
        else:
            bulk_download_path = item["path"].replace("_", " ")

        PrepaidAgreement.objects.update_or_create(
            pk=pk,
            defaults={
                "product": product,
                "created_time": created_time,
                "effective_date": effective_date,
                "compressed_files_url": url,
                "bulk_download_path": bulk_download_path,
                "filename": item["agreements_files_location"],
            },
        )


def run(*args):
    source_url = S3_PATH + METADATA_FILENAME
    resp = requests.get(url=source_url)
    data = resp.json()

    imported_products = import_products_data(data["products"])
    import_agreements_data(data["agreements"])
    mark_deleted_products(imported_products)
