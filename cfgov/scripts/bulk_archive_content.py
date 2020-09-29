import logging

from django.db import transaction
from django.http import Http404
from django.utils import timezone

from wagtail.core.models import Site

from dateutil.relativedelta import relativedelta


logger = logging.getLogger(__name__)


# This script is for use on September 30, 2020, to perform a bulk archive of
# content in the Newsroom, Blog, and Research & Reports. This script can be
# deleted after that archival is performed.
# Run from the command-line with the URL of a filterable list page to archive:
#   cfgov/manage.py runscript bulk_archive_content --script-args [URL PATH]
def run(*args):
    if not args:
        logger.error("error. Use --script-args [URL PATH] to specify the " +
                     "URL path of a filterable list page the content of which "
                     "needs to be archived if its last published date is 2 "
                     "years or more in the past.")
    else:
        path = args[0]
        path_components = path.split('/')

        # Get the filterable list page
        default_site = Site.objects.get(is_default_site=True)
        root_page = default_site.root_page

        try:
            filterable_page = root_page.route(None, path_components).page
        except Http404:
            logger.error(f"Unable to find a filterable list page for {path}. "
                         "Ensure that the path is correct, and leave off any "
                         "leading or trailing / characters.")
            return

        archived_at = timezone.now()
        cutoff_date = archived_at - relativedelta(years=2)

        # Get the queryset and filter it on last_published_at.
        filtered_pages = filterable_page.get_filterable_queryset().filter(
            last_published_at__lt=cutoff_date,
            is_archived=False
        )

        logger.info(
            f"Archiving {filtered_pages.count()} pages within "
            f"{filterable_page.title} older than {cutoff_date}"
        )

        with transaction.atomic():
            update_count = filtered_pages.select_for_update().update(
                is_archived=True,
                archived_at=archived_at
            )

        logger.info(f"Archived {update_count} pages")
