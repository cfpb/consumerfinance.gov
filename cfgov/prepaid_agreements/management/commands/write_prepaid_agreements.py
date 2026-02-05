import csv
import logging
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

from django.core.management.base import BaseCommand

import boto3

from prepaid_agreements.models import PrepaidAgreement


logger = logging.getLogger(__name__)


def generate_agreements_data():
    agreements_fieldnames = [
        "issuer_name",
        "product_name",
        "product_id",
        "agreement_effective_date",
        "agreement_id",
        "most_recent_agreement",
        "created_date",
        "current_status",
        "withdrawal_date",
        "prepaid_product_type",
        "program_manager_exists",
        "program_manager",
        "other_relevant_parties",
        "path",
        "direct_download",
    ]
    products_fieldnames = [
        "issuer_name",
        "product_name",
        "product_id",
        "agreement_effective_date",
        "agreement_id",
        "created_date",
        "current_status",
        "withdrawal_date",
        "prepaid_product_type",
        "program_manager_exists",
        "program_manager",
        "other_relevant_parties",
        "path",
        "direct_download",
    ]

    agreements_buffer = StringIO()
    products_buffer = StringIO()

    # Write a BOM at the top of the file so Excel knows it's UTF-8
    agreements_buffer.write("\ufeff")
    products_buffer.write("\ufeff")

    agreements_writer = csv.DictWriter(
        agreements_buffer, fieldnames=agreements_fieldnames
    )
    agreements_writer.writeheader()

    products_writer = csv.DictWriter(
        products_buffer, fieldnames=products_fieldnames
    )
    products_writer.writeheader()

    agreements = sorted(
        PrepaidAgreement.objects.all(),
        key=lambda agreement: (
            agreement.product.issuer_name,
            agreement.product.name,
            agreement.product.pk,
            agreement.created_time,
        ),
    )

    agreements_counter = 0
    products_counter = 0
    for agreement in agreements:
        product = agreement.product
        # CSV should only includes data that has not been marked for
        # deletion
        if product.deleted_at is None:
            most_recent = "Yes" if agreement.is_most_recent else "No"
            created_time = agreement.created_time.strftime("%Y-%m-%d %H:%M:%S")

            other_relevant_parties = product.other_relevant_parties
            if other_relevant_parties:
                other_relevant_parties = other_relevant_parties.replace(
                    "\n", "; "
                )
            else:
                other_relevant_parties = "No information provided"

            data = {
                "issuer_name": product.issuer_name,
                "product_name": product.name,
                "product_id": product.pk,
                "agreement_effective_date": agreement.effective_date,
                "created_date": created_time,
                "withdrawal_date": product.withdrawal_date,
                "current_status": product.status,
                "prepaid_product_type": product.prepaid_type,
                "program_manager_exists": product.program_manager_exists,
                "program_manager": product.program_manager,
                "other_relevant_parties": other_relevant_parties,
                "path": agreement.bulk_download_path,
                "direct_download": agreement.compressed_files_url,
                "agreement_id": agreement.pk,
            }

            # Product-level CSV only includes data
            # for a product's most recent agreement,
            # such that there is one row per product ID
            if agreement.is_most_recent:
                products_writer.writerow(data)
                products_counter += 1

            data["most_recent_agreement"] = most_recent
            agreements_writer.writerow(data)
            agreements_counter += 1

    logger.info(
        f"Wrote {agreements_counter} agreements, {products_counter} products"
    )

    return agreements_buffer.getvalue(), products_buffer.getvalue()


class Command(BaseCommand):
    """
    Write prepaid card agreement and product data to CSV files
    """

    help = "Write prepaid card agreement and product data to CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            action="store",
            required=True,
            help=(
                "Local directory or S3 URL (s3://bucket/prefix) into which "
                "two CSV files of prepaid agreements and product data will "
                "be written."
            ),
        )

    def handle(self, *args, **options):
        path = options["path"]

        agreements_data, products_data = generate_agreements_data()
        agreements_filename = "prepaid_metadata_all_agreements.csv"
        products_filename = "prepaid_metadata_recent_agreements.csv"

        if path.startswith("s3://"):
            s3_url = urlparse(path)
            self.write_to_s3(s3_url, agreements_filename, agreements_data)
            self.write_to_s3(s3_url, products_filename, products_data)
        else:
            path = Path(path)
            self.write_to_directory(path, agreements_filename, agreements_data)
            self.write_to_directory(path, products_filename, products_data)

    def write_to_directory(self, path, filename, data):
        with open(path / filename, "w", encoding="utf-8") as f:
            f.write(data)
        logger.info(f"Wrote {filename} to {path}")

    def write_to_s3(self, s3_url, filename, data):
        bucket = s3_url.netloc
        prefix = s3_url.path.strip("/")
        s3 = boto3.client("s3")
        key = f"{prefix}/{filename}" if prefix else filename
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=data.encode("utf-8"),
            ContentType="text/csv",
        )
        logger.info(f"Wrote {filename} to s3://{bucket}/{key}")
