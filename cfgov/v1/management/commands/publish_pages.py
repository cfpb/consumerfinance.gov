# Publish Wagtail pages given a list of relative URLs in a file.
#
# Usage:
#
#    manage.py publish_pages
#       [--dry-run]
#       [--ignore-missing]
#       input.txt
#
#    --dry-run: Only read file and validate URLs, don't publish anything
#    --ignore-missing: Ignore any invalid URLs in the input file
#
# Expected input file format:
#
#    /path/to/page1/
#    /path/to/page2/
#    ...

import argparse

from django.core.management import BaseCommand
from django.http import Http404
from django.test import RequestFactory

from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Site


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
            help="Only read file and validate URLs, don't publish anything",
        )
        parser.add_argument(
            "--ignore-missing",
            action="store_true",
            help="Ignore any invalid URLs in the input file",
        )

    def handle(self, *args, **options):
        for relative_url in options["filename"]:
            try:
                page = self.route(relative_url.strip())
            except Http404:
                if options["ignore_missing"]:
                    continue
                else:
                    raise

            page = page.get_latest_revision_as_object()

            if not options["dry_run"]:
                page.save_revision().publish()

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
