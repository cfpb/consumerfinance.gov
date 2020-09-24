import csv
import logging

from wagtail.core.models import Page


logger = logging.getLogger(__name__)


# This script is for use on September 30, 2020, when we'll be migrating
# cf.gov to a new IA. Delete this script after the migration is done.
# Run this from the command line with this:
#   cfgov/manage.py runscript pages_to_redirect --script-args [PATH]
def run(*args):
    if not args:
        logger.error("error. Use --script-args [PATH] to specify the " +
                     "location of the csv.")
    else:
        page_moves_file = args[0]
        redirects_file = 'redirects_list.csv'

        pages_to_move = set()

        with open(page_moves_file, "r") as csv_file:
            page_list = csv.reader(csv_file, delimiter=',')
            next(page_list)  # skip the header row

            # Edit this list to match the headers of the input file, just
            # make sure page_id and redirect are included
            for [redirect, _, _, page_id, _, _, _, _, _] in page_list:
                # Get the set of pages that will need wagtail redirects
                if redirect == 'TRUE':
                    page = Page.objects.get(id=page_id)
                    live_descendants = \
                        page.get_descendants(True).filter(live=True)
                    pages_to_move = pages_to_move.union(live_descendants)

            pages_to_move = sorted(pages_to_move, key=lambda pg: pg.id)
            ids = [pg.id for pg in pages_to_move]
            logger.info(f"IDs of pages to redirect: {ids}")
            logger.info(f"Total pages: {len(ids)}")

        with open(redirects_file, "w") as output_file:
            redirects_list = csv.writer(output_file)
            for page in pages_to_move:
                row = [page.url, page.id]
                redirects_list.writerow(row)

        logger.info(f"Generated redirects CSV at: {redirects_file}")
