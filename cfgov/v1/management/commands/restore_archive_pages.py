from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.utils import timezone

from wagtail.core.models import Site

from dateutil.relativedelta import relativedelta

from v1.management.commands.archive_pages import (
    path_without_leading_trailing_slashes
)


class Command(BaseCommand):
    help = "Mark archived pages within a filterable list as restored"

    def add_arguments(self, parser):
        parser.add_argument(
            "url_path",
            nargs="+",
            type=path_without_leading_trailing_slashes,
            help=(
                "The URL path (without leading /) of a filterable list page "
                "whose content should be restored if it was archived the "
                "specified number of years, months, and days ago. "
                "The filterable list page at the URL will not be restored."
            ),
        )
        parser.add_argument(
            "--years",
            type=int,
            default=2,
            help=(
                "Restore content archived this number of years ago. "
                "Combines with --months --days. Default: 2"
            ),
        )
        parser.add_argument(
            "--months",
            type=int,
            default=0,
            help=(
                "Restore content archived this number of months ago. "
                "Combines with --years --days. Default: 0"
            ),
        )
        parser.add_argument(
            "--days",
            type=int,
            default=0,
            help=(
                "Restore content archived this number of days ago. "
                "Combines with --years --months. Default: 0"
            ),
        )
        parser.add_argument(
            "--by-published-date",
            choices=["first", "last"],
            default="first",
            help=(
                "Restore based on either first or last published date. "
                "Default: first"
            ),
        )

    def handle(self, *args, **options):
        url_paths = options["url_path"]

        # Get the current date/time and then get our cutoff date for restoring
        # based on it.
        archived_at = timezone.now()
        cutoff_date = archived_at - relativedelta(
            years=options["years"],
            months=options["months"],
            days=options["days"],
        )

        # Construct a Q object to filter on based on this command-line
        # argument.
        if options["by_published_date"] == "last":
            published_date_filter = Q(last_published_at__lt=cutoff_date)
        else:
            published_date_filter = Q(first_published_at__lt=cutoff_date)

        # We'll use Wagtail's page routing to resolve the page at the given the
        # URL paths.
        default_site = Site.objects.get(is_default_site=True)
        root_page = default_site.root_page

        for path in url_paths:
            path_components = path.split("/")

            # Get the filterable list page we're interested in.
            try:
                filterable_page = root_page.route(None, path_components).page
            except Http404:
                raise CommandError(
                    f"Unable to find a page at {path}. "
                    "Ensure that the path is correct, and leave off any "
                    "leading or trailing / characters."
                )

            # Get the filterable list QuerySet and filter it.
            filtered_pages = filterable_page.get_filterable_queryset().filter(
                published_date_filter,
                is_archived="yes",
            )

            # Restore the content, letting the user know the title of the
            # filterable list page, the cuttoff date and how many pages will be
            # restored.
            with transaction.atomic():
                update_count = filtered_pages.select_for_update().update(
                    is_archived="no",
                    archived_at=archived_at
                )
            self.stdout.write(
                f"Found and restored {update_count} pages within "
                f"{filterable_page.title} older than "
                f"{cutoff_date:%Y-%m-%d %H:%M %Z}. "
            )
