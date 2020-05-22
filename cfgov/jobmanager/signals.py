import logging

from wagtail.core.signals import page_published

import requests
from flags.state import flag_enabled

from jobmanager.models.pages import JobListingPage


logger = logging.getLogger(__name__)


SITEMAP_URL = 'https://www.consumerfinance.gov/sitemap.xml'
GOOGLE_URL = 'https://www.google.com/ping'


def request_site_recrawl(sender, **kwargs):
    try:
        if flag_enabled('PING_GOOGLE_ON_PUBLISH'):
            response = requests.get(GOOGLE_URL, {'sitemap': SITEMAP_URL})
            response.raise_for_status()
            logger.info(
                'Pinged Google after job page publication.'
            )
    except Exception:
        logger.exception(
            'Pinging Google after job page publication failed.'
        )


def register_signal_handlers():
    page_published.connect(request_site_recrawl, sender=JobListingPage)
