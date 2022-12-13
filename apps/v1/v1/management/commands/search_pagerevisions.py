import csv

from django.core.management.base import BaseCommand
from django.urls import reverse

from wagtail.core.models import Page
from wagtail.search.backends import get_search_backend

from v1.models import IndexedPageRevision


class Command(BaseCommand):
    help = "Search for a particular string within page revisions"

    def add_arguments(self, parser):
        parser.add_argument(
            "search string", help="Words to search for within page revisions"
        )
        parser.add_argument(
            "--filename",
            help="Export the results to a CSV file instead of to stdout",
        )

    def handle(self, *args, **kwargs):
        search_backend = get_search_backend("fulltext")
        revision_results = search_backend.search(
            kwargs["search string"], IndexedPageRevision
        )

        filename = kwargs["filename"]
        if not filename:
            # Ensure stdout can't be closed by the context manager below
            self.stdout.close = lambda: None

        with (
            open(filename, "w", newline="", encoding="utf-8")
            if filename
            else self.stdout
        ) as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Page id",
                    "Revision id",
                    "Preview URL",
                    "Revision created date",
                ]
            )
            writer.writerows(
                [
                    (
                        r.page_id,
                        r.id,
                        reverse(
                            "wagtailadmin_pages:revisions_view",
                            args=(r.page_id, r.id),
                        ),
                        r.created_at.isoformat(),
                    )
                    for r in revision_results
                    if Page.objects.filter(id=r.page_id).exists()
                ]
            )
