import csv
import logging

from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Page


logger = logging.getLogger(__name__)


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
        total = 0

        # Edit this list to match the headers of the input file, just
        # make sure page_id and redirect are included
        headers = [page_id, destination_id, xlug, redirect]


        with open(page_moves_file, "r") as csv_file:
            page_list = csv.reader(csv_file, delimiter=',')
            next(page_list)  # skip the header row
            for headers in page_list:
                # Get the set of pages that will need wagtail redirects
                if redirect == 'TRUE':
                    page = Page.objects.get(id=page_id)
                    live_descendants = page.get_descendants(True).filter(live=True)
                    pages_to_move = pages_to_move.union(live_descendants)

            ids = [pg.id for pg in pages_to_move]
            logger.info("IDs of pages to move: ", ids)
            logger.info("Total pages: ", len(pages_to_move))

        with open(redirects_file, "w") as output_file:
            redirects_list = csv.writer(output_file)
            for page in pages_to_move:
                row = [page.url, page.i]
                redirects_list.writerow(row)
