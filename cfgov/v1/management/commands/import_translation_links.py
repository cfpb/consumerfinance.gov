# Import page translation links from a CSV file with format:
#
#    translated_page_relative_url,english_relative_url
#
# By default only saves translation link as a new page revision.
#
# If --republish is specified, pages whose most recent revision
# is already live will have the new revision published as well.
# If a page is live but already has a draft revision saved,
# a new draft revision will be saved with the translation link.
#
# Usage:
#
#    manage.py import_translation_links
#       [--dry-run]
#       [--revision-username REVISION_USERNAME]
#       [--republish]
#       input.csv
#
#    --dry-run: Only read CSV, don't save anything
#    --revision-username: username used for new revisions
#    --republish: Republish already-live pages

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
        parser.add_argument("filename", type=argparse.FileType("r"))
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only read CSV, don't save anything",
        )
        parser.add_argument(
            "--revision-username", help="Username used for new revisions"
        )
        parser.add_argument(
            "--republish",
            action="store_true",
            help="Republish already-live pages",
        )

    def handle(self, *args, **options):
        reader = csv.reader(options["filename"])

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
            translated_page = self.route(translated_relative_url)
            english_page = self.route(english_relative_url)

            has_unpublished_changes = translated_page.has_unpublished_changes
            translated_page.english_page = english_page

            if not options["dry_run"]:
                revision = translated_page.save_revision(
                    user=revision_user, log_action=True
                )
                if (
                    options["republish"]
                    and translated_page.live
                    and not has_unpublished_changes
                ):
                    revision.publish()

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
