# Import page translation links from a CSV file with format:
#
#    translated_page_relative_url,english_relative_url
#
# By default only saves translation link as a new page revision.
#
# If --publish is specified, the new revision will be published.
#
# If --republish-only is also specified, only pages whose most recent
# revision is already live will have the new revision published.
#
# Usage:
#
#    manage.py import_translation_links
#       [--dry-run]
#       [--revision-username REVISION_USERNAME]
#       [--publish]
#       [--republish-only]
#       [--ignore-missing]
#       input.csv
#
#    --dry-run: Only read CSV, don't save anything
#    --revision-username: Username used for new revisions
#    --publish: Publish new revisions
#    --republish-only: Only publish pages without existing drafts
#    --ignore-missing: Ignore any invalid URLs in the input CSV
#    --skip-header: Skip first row of input CSV

import argparse
import csv

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError
from django.http import Http404
from django.test import RequestFactory

from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Site


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.site = Site.objects.get(is_default_site=True)
        self.site_root = self.site.root_page
        self.request_factory = RequestFactory()

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", type=argparse.FileType("r", encoding="utf-8-sig")
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only read CSV, don't save anything",
        )
        parser.add_argument(
            "--revision-username", help="Username used for new revisions"
        )
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Publish new revisions",
        )
        parser.add_argument(
            "--republish-only",
            action="store_true",
            help="Only publish pages without existing drafts",
        )
        parser.add_argument(
            "--ignore-missing",
            action="store_true",
            help="Ignore any invalid URLs in the input CSV",
        )
        parser.add_argument(
            "--skip-header",
            action="store_true",
            help="Skip first row of input CSV",
        )

    def handle(self, *args, **options):
        reader = csv.reader(options["filename"])

        if options["skip_header"]:
            next(reader)

        dry_run = options["dry_run"]
        revision_username = options["revision_username"]
        revision_user = None

        if not revision_username:
            if not dry_run:
                raise CommandError(
                    "Must specify --revision-username if not using --dry-run"
                )
        else:
            User = get_user_model()
            revision_user = User.objects.get(username=revision_username)

        for translated_relative_url, english_relative_url in reader:
            try:
                translated_page = self.route(translated_relative_url.strip())
                english_page = self.route(english_relative_url.strip())
            except Http404:
                if options["ignore_missing"]:
                    continue
                else:
                    raise

            is_live = translated_page.live
            has_unpublished_changes = translated_page.has_unpublished_changes

            translated_page = translated_page.get_latest_revision_as_page()
            translated_page.english_page = english_page

            if not options["dry_run"]:
                revision = translated_page.save_revision(
                    user=revision_user, log_action=True
                )

                if options["publish"]:
                    if options["republish_only"] and (
                        (not is_live) or has_unpublished_changes
                    ):
                        continue

                    revision.publish(user=revision_user)

    def route(self, relative_url):
        try:
            return self._route(relative_url)
        except Http404:
            try:
                redirect = Redirect.get_for_site(self.site).get(
                    old_path=Redirect.normalise_path(relative_url)
                )
            except Redirect.DoesNotExist:
                pass
            else:
                if redirect and redirect.redirect_page:
                    return redirect.redirect_page.specific

        raise Http404(relative_url)

    def _route(self, relative_url):
        request = self.request_factory.get(relative_url)
        path_components = [
            component for component in relative_url.split("/") if component
        ]

        page, _, __ = self.site_root.localized.specific.route(
            request, path_components
        )

        return page
