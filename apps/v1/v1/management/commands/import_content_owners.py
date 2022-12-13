# Run with:
#
#   cfgov/manage.py import_content_owners owners.csv
#
# To save a log and time how long this takes:
#
#   time cfgov/manage.py import_content_owners owners.csv > log.txt 2>&1
#
# owners.csv should be in the format:
#
#   "/path/to/page/","owner1"
#   "/path/to/other/page/","owner1,owner2"
import argparse
import csv
import json
from itertools import chain
from operator import itemgetter

from django.core.management import BaseCommand
from django.http.response import Http404
from django.test import RequestFactory

from wagtail.core.models import Site

from v1.models.base import CFGOVContentOwner


class Command(BaseCommand):
    help = "Import Wagtail page content owners"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.factory = RequestFactory()
        self.site = Site.objects.get(is_default_site=True)

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", type=argparse.FileType("r", encoding="utf-8-sig")
        )

    def handle(self, *args, **options):
        reader = csv.reader(options["filename"])
        url_owners = list(reader)

        # Strip out header line or URLs without any owners.
        url_owners = [
            (url, owners)
            for url, owners in url_owners
            if url and owners and (url, owners) != ("url", "owner")
        ]

        # First, ensure that all owner tags are created, and cache their IDs.
        owner_names = set(chain(map(itemgetter(1), url_owners)))

        for owner_name in owner_names:
            CFGOVContentOwner.objects.get_or_create(name=owner_name)

        owner_pks_by_name = dict(
            CFGOVContentOwner.objects.values_list("name", "pk")
        )

        # Now, go through each URL and update the page and its revisions.
        for i, (url, owners) in enumerate(url_owners):
            print(f"{i} / {len(url_owners)}: {url}")

            try:
                page = self.get_page(url)
            except Http404:
                self.stderr.write(f"No page at URL {url}, skipping.")

            owners = owners.split(",")

            print(f"Setting owners for page {page.pk}: {owners}")

            for owner in owners:
                page.content_owners.add(owner)

            page.save(update_fields=["cfgovownedpages_set"])

            revision_count = page.revisions.count()

            for j, revision in enumerate(page.revisions.all()):
                print(
                    f"\t{j} / {revision_count}: "
                    f"Setting owners for revision {revision.pk}"
                )
                revision_content = json.loads(revision.content_json)

                revision_owners = [
                    {
                        "pk": None,
                        "tag": owner_pks_by_name[owner],
                        "content_object": page.pk,
                    }
                    for owner in owners
                ]

                revision_content["cfgovownedpages_set"] = revision_owners
                revision.content_json = json.dumps(revision_content)

                revision.save(update_fields=["content_json"])

    def get_page(self, path):
        request = self.factory.get(path)

        path_components = [c for c in path.split("/") if c]
        page, _, __ = self.site.root_page.localized.specific.route(
            request, path_components
        )

        return page
