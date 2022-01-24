import logging
import os


from django.db import transaction

from wagtail.core.models import Page, Site
from wagtailsharing.models import SharingSite

from v1.models import HomePage, SublandingPage
from regulations3k.models.pages import RegulationLandingPage, RegulationsSearchPage
from scripts.initial_data import run as initial_data

logger = logging.getLogger(__name__)


@transaction.atomic
def add_regulations_search_data(home_page):
    logger.info('Adding data for regulations-search tests')

    # Check to see if the top-level "Rules & Policy" page exists, and create
    # it if not.
    try:
        rules_policy_page = SublandingPage.objects.get(slug='rules-policy')
    except SublandingPage.DoesNotExist:
        logger.info('Creating Rules & Policy page')

        # Create the new home page instance.
        rules_policy_page = SublandingPage(
            title='Rules & Policy',
            slug='rules-policy',
            live=True
        )

        # Add the page as a child to the home page
        home_page.add_child(instance=rules_policy_page)

    # See if the Interactive Regs landing page exists, and create it if not.
    try:
        interactive_regs_page = RegulationLandingPage.objects.get(
            slug='regulations'
        )
    except RegulationLandingPage.DoesNotExist:
        logger.info('Creating Interactive Bureau Regulations landing page')

        # Create the new home page instance.
        interactive_regs_page = RegulationLandingPage(
            title='Interactive Bureau Regulations',
            slug='regulations',
            live=True
        )

        # Add the page as a child to the home page
        rules_policy_page.add_child(instance=interactive_regs_page)

    # See if the Interactive Regs search page exists, and create it if not.
    try:
        search_page = RegulationsSearchPage.objects.get(
            slug='search-regulations'
        )
    except RegulationsSearchPage.DoesNotExist:
        logger.info('Creating Interactive Bureau Regulations landing page')

        # Create the new home page instance.
        search_page = RegulationsSearchPage(
            title='Search regulations',
            slug='search-regulations',
            live=True
        )

        # Add the page as a child to the home page
        interactive_regs_page.add_child(instance=search_page)



@transaction.atomic
def run():
    initial_data()

    logger.info('Running script test_data')

    default_site = Site.objects.get(is_default_site=True)
    home_page = HomePage.objects.get(slug='cfgov')

    add_regulations_search_data(home_page)
