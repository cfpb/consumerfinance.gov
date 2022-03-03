# This is a one-time script which can be deleted after running. March 2021.
# This script executes a data migration to make a correction to Enforcement
# Action Pages. It adds "fair lending" to the list of products on any page
# that had "fair lending" as an at-risk group and makes other corrections to
# the product list for enforcement action pages.
# Prerequisite: Run the migration that adds "fair lending" as a product choice
import csv
import logging
import sys

from v1.models.enforcement_action_page import (
    EnforcementActionPage,
    EnforcementActionProduct,
)

logger = logging.getLogger(__name__)


def run(*args):
    if not args or len(args) != 1:
        logger.error(
            "error. Use --script-args [CSV_PATH] "
            + "to specify the location of the data csv."
        )
        sys.exit()

    data_file = args[0]

    with open(data_file, "r", encoding="utf-8-sig") as csv_file:
        rows = csv.reader(csv_file, delimiter=",")
        for _, products, path in rows:
            try:
                page = EnforcementActionPage.objects.get(url_path=path)
            except EnforcementActionPage.DoesNotExist:
                logger.warn(f"invalid url path: {path}")
                continue

            expected_products = sorted(
                [p.strip() for p in products.split(";")]
            )  # noqa: B950
            actual_products = sorted(
                [product.product for product in page.products.all()]
            )  # noqa: B950
            if expected_products == actual_products:
                continue
            else:
                logger.info(f"fixing products on {page.title}")
                for e in expected_products:
                    if e not in actual_products:
                        new = EnforcementActionProduct(product=e, action=page)
                        new.save()

                for p in page.products.all():
                    if p.product not in expected_products:
                        p.delete()
                page.save

        logger.info("Completed!")
