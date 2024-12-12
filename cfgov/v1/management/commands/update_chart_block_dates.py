import json
import logging
import os
from datetime import datetime

from django.core.management.base import BaseCommand

from v1.models import CFGOVPage
from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_changes


logger = logging.getLogger(__name__)

notes_stub = (
    "Data from the last six months are not final. "
    "The most recent data available in this graph are for "
)


def human_date(machine_date):
    d = datetime.strptime(machine_date, "%Y-%m-%d")
    return d.strftime("%B %Y")


def get_inquiry_month(data, data_source):
    for item in data:
        month = None
        if item["market_key"] in data_source:
            if "inq_" in data_source:
                month = item["inquiry_month"]
                break
            elif "crt_" in data_source:
                month = item["tightness_month"]
                break
    return month


class Command(BaseCommand):
    help = "Monthly updates to data snapshot values"

    def expand_path(self, path):
        """Expands a relative path into an absolute path"""
        rootpath = os.path.abspath(os.path.expanduser(path))

        return rootpath

    def add_arguments(self, parser):
        """Adds all arguments to be processed."""
        parser.add_argument(
            "--snapshot_file",
            required=True,
            help="JSON file containing all markets' data snapshot values",
        )

    def update_chart_blocks(self, date_published, last_updated, markets):
        """Update date_published on all chart blocks"""

        cct_landing_page = CFGOVPage.objects.get(
            slug="consumer-credit-trends"
        ).specific

        for page in BrowsePage.objects.live().descendant_of(cct_landing_page):
            chart_blocks = list(
                filter(
                    lambda item: item["type"] == "chart_block",
                    page.specific.content.raw_data,
                )
            )

            simple_chart_blocks = list(
                filter(
                    lambda item: item["type"] == "simple_chart",
                    page.specific.content.raw_data,
                )
            )

            for chart in simple_chart_blocks:
                chart["value"]["notes"] = notes_stub + human_date(last_updated)
                chart["value"]["date_published"] = human_date(date_published)

            for chart in chart_blocks:
                chart_options = chart["value"]
                chart["value"]["date_published"] = date_published
                if chart_options["chart_type"] == "line-index":
                    last_updated_inquiry = get_inquiry_month(
                        markets, chart_options["data_source"]
                    )
                    chart["value"]["last_updated_projected_data"] = (
                        last_updated_inquiry
                    )
                else:
                    chart["value"]["last_updated_projected_data"] = (
                        last_updated
                    )

            if chart_blocks or simple_chart_blocks:
                publish_changes(page.specific)

    def handle(self, *args, **options):
        # Read in CCT snapshot data from json file
        with open(self.expand_path(options["snapshot_file"])) as json_data:
            data = json.load(json_data)

        markets = data["markets"]
        date_published = data["date_published"]
        last_updated = max([item["data_month"] for item in markets])
        inquiry_activity_charts = [
            item for item in markets if "inquiry_month" in item
        ]

        self.update_chart_blocks(
            date_published, last_updated, inquiry_activity_charts
        )
