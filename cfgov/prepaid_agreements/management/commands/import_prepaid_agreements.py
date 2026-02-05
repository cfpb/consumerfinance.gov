import logging
from datetime import datetime
from urllib.parse import quote, urljoin

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

import requests
import zoneinfo

from prepaid_agreements.models import PrepaidAgreement, PrepaidProduct


S3_URL = (
    f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/a/assets/prepaid-agreements/"
)
METADATA_FILENAME = "prepaid_metadata.json"

logger = logging.getLogger(__name__)


def mark_deleted_products(valid_products):
    PrepaidProduct.objects.exclude(pk__in=valid_products).exclude(
        deleted_at__isnull=False
    ).update(deleted_at=timezone.now())


def import_products_data(products_data):
    imported_products = []
    for item in products_data:
        pk = item["product_id"].replace("PRODUCT-", "").replace("AGMNT-", "")
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
    logger.info(f"Imported {len(imported_products)} products")
    return imported_products


def import_agreements_data(agreements_data, base_url):
    for item in agreements_data:
        pk = item["agreement_id"].replace("IFL-", "").replace("AGMNT-", "")
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
        created_time = created_time.replace(tzinfo=zoneinfo.ZoneInfo("EST"))

        product_id = (
            item["product_id"].replace("PRODUCT-", "").replace("AGMNT-", "")
        )
        product = PrepaidProduct.objects.get(pk=product_id)
        url = urljoin(base_url, quote(item["agreements_files_location"]))

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

    logger.info(f"Imported {len(agreements_data)} agreements")


class Command(BaseCommand):
    """
    Imports prepaid card agreement data from a URL in S3
    """

    help = "Import prepaid agreements data from an S3 URL."

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--base-url",
            action="store",
            default=S3_URL,
            help="URL to the prepaid agreements files in S3",
        )
        parser.add_argument(
            "-m",
            "--metadata-filename",
            action="store",
            default=METADATA_FILENAME,
            help="Metadata filename ",
        )

    def handle(self, *args, **options):
        base_url = options["base_url"]
        metadata_filename = options["metadata_filename"]

        source_url = urljoin(base_url, metadata_filename)
        logger.info(f"Fetching metadata from {source_url}")

        resp = requests.get(url=source_url)
        data = resp.json()

        logger.info("Importing products")
        imported_products = import_products_data(data["products"])
        logger.info("Importing agreements")
        import_agreements_data(data["agreements"], base_url)

        logger.info("Marking deleted products")
        mark_deleted_products(imported_products)
