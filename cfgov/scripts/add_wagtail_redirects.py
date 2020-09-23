import csv
import logging

from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Page


logger = logging.getLogger(__name__)


# This script is for use on September 30, 2020, when we'll be migrating
# cf.gov to a new IA. Delete this script after the migration is done.
# Run this from the command line with this:
#   cfgov/manage.py runscript add_wagtail_redirects --script-args [PATH]
def run(*args):
    if not args:
        logger.error("error. Use --script-args [PATH] to specify the " +
                     "location of the redirects csv.")
    else:
        redirects_file = args[0]

        dupes = []
        successes = 0
        deletes = 0

        with open(redirects_file, "r") as csv_file:
            redirect_list = csv.reader(csv_file, delimiter=',')
            for [from_url, to_id] in redirect_list:
                # If conflicting redirects exist for this from_url, delete them
                existing_redirects = Redirect.objects.filter(
                    old_path__iexact=Redirect.normalise_path(from_url))
                if len(existing_redirects) > 0:
                    dupes.append(from_url)
                    num, _ = existing_redirects.delete()
                    deletes += num

                # Add the desired redirect
                page = Page.objects.get(id=to_id)
                Redirect.add_redirect(from_url, redirect_to=page,
                                      is_permanent=True)
                successes += 1

        logger.info(f"Done! Added {successes} redirects")
        if len(dupes) > 0:
            logger.debug(f"Redirects already existed for these urls: {dupes}")
            logger.info(f"Replaced {deletes} redirects with updated ones")
