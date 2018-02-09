import requests

from wagtail.wagtailcore.signals import page_published

from flags.state import flag_enabled

from jobmanager.models.pages import JobListingPage

SITEMAP_URL = 'https://www.consumerfinance.gov/sitemap.xml'
GOOGLE_URL = 'http://www.google.com/ping'


def request_site_recrawl(sender, **kwargs):
    try:
        if flag_enabled('PING_GOOGLE'):
            requests.get(GOOGLE_URL, {'sitemap': SITEMAP_URL})
    except:
        pass


page_published.connect(request_site_recrawl, sender=JobListingPage)
