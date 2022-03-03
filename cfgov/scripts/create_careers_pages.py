import logging

from django.db import transaction

from wagtail.core.models import Page, Site

from v1.models import BrowsePage, LandingPage, SublandingPage
from v1.tests.wagtail_pages.helpers import save_new_page

logger = logging.getLogger(__name__)


@transaction.atomic
def run():
    default_site = Site.objects.get(is_default_site=True)
    root_page = default_site.root_page

    try:
        about_us = Page.objects.get(slug="about-us")
    except Page.DoesNotExist:
        logger.info("Creating page: About Us")
        about_us = LandingPage(title="About Us", slug="about-us", live=False)
        save_new_page(about_us, root=root_page)

    try:
        careers = Page.objects.get(slug="careers")
    except Page.DoesNotExist:
        logger.info("Creating page: Careers")
        careers = SublandingPage(title="Careers", slug="careers", live=False)
        save_new_page(careers, root=about_us)

    child_pages = [
        ("Working at the CFPB", "working-at-cfpb"),
        ("Job Application Process", "application-process"),
        ("Students and Graduates", "students-and-graduates"),
        ("Current Openings", "current-openings"),
    ]

    for title, slug in child_pages:
        try:
            child_page = Page.objects.get(slug=slug)
        except Page.DoesNotExist:
            logger.info("Creating page: {}".format(title))
            child_page = BrowsePage(title=title, slug=slug, live=False)
            save_new_page(child_page, careers)


if "__main__" == __name__:
    run()
