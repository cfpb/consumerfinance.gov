import csv
import logging

from wagtail.core.models import Page


logger = logging.getLogger(__name__)


# Run this from the command line with this:
#   cfgov/manage.py runscript move_wagtail_pages --script-args [PATH]
def run(*args):
    if not args:
        logger.error("error. Use --script-args [PATH] to specify the " +
                     "location of the csv.")
    else:
        page_moves_file = args[0]

        successes = 0

        with open(page_moves_file, "r") as csv_file:
            page_list = csv.reader(csv_file, delimiter=',')
            next(page_list)  # skip the header row

            # Edit this list to match the headers of the input file, just
            # make sure page_id, destination_id, new_slug are included
            for [_, _, new_slug, page_id, _, _, _, destination_id, _] in page_list:
                page = Page.objects.get(id=page_id)
                if new_slug:
                    page.slug = new_slug
                    page.save()
                new_parent = Page.objects.get(id=destination_id)
                page.move(new_parent, pos='first-child')
                successes += 1

        logger.info(f"Done! Moved {successes} top-level pages")
