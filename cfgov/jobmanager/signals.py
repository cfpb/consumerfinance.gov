import logging
import os
import requests

from wagtail.wagtailcore.signals import page_published

from jobmanager.models.pages import JobListingPage

logger = logging.getLogger(__name__)


def request_site_recrawl(sender, **kwargs):
    sitemap_url = os.environ.get('SITEMAP_URL')
    google_url = os.environ.get('GOOGLE_PING_URL')

    try:
        if sitemap_url and google_url:
            requests.get(google_url, {'sitemap': sitemap_url})
            logger.info(
                'Pinged Google after job page publication.'
            )
    except Exception:
        logger.exception(
            'Pinging Google after job page publication failed.'
        )


page_published.connect(request_site_recrawl, sender=JobListingPage)
