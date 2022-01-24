import logging
import os


from django.db import transaction

from wagtail.core.models import Page, Site
from wagtailsharing.models import SharingSite

from v1.models import HomePage
from scripts.initial_data import run as initial_data

logger = logging.getLogger(__name__)


@transaction.atomic
def run():
    initial_data()

    logger.info('Running script test_data')

    default_site = Site.objects.get(is_default_site=True)
    home_page = HomePage.objects.get(slug='cfgov')
