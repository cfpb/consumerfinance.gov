import logging
import urllib2
import requests
import json
import os

from bs4 import BeautifulSoup

from jobmanager.models.pages import JobListingPage

logger = logging.getLogger(__name__)

URL = os.environ.get('USAJOBS_ARCHIVE_URL')
HEADERS = {
    'Host': os.environ.get('USAJOBS_HOST'),
    'User-Agent': os.environ.get('USAJOBS_USER'),
    'Authorization-Key': os.environ.get('USAJOBS_API_KEY'),
}


def job_page_closed(link):
    webpage = urllib2.urlopen(link)
    soup = BeautifulSoup(webpage, 'html.parser')
    closed_text = soup.find('div', attrs={'class': 'usajobs-joa-closed'})
    if closed_text:
        return 'This job announcement has closed' in closed_text.contents


def job_archived(link):
    try:
        control_number = os.path.basename(os.path.normpath(link))
        response = requests.get(URL, headers=HEADERS, params={
            'ControlNumber': control_number,
            'WhoMayApply': 'all'
        })
        results = json.loads(response.text)['SearchResult']
        search_items = results['SearchResultItems']
        return search_items[0]['MatchedObjectId'] == control_number
    except:
        pass


def run():
    logger.info('Searching for live job posting pages...')

    job_pages = JobListingPage.objects.filter(live=True)

    if job_pages:
        for page in job_pages:
            if page.usajobs_application_links:
                closed_count = 0
                links = page.usajobs_application_links.all()
                for link in links:
                    if job_archived(link.url) or job_page_closed(link.url):
                        closed_count += 1
                if closed_count and closed_count == links.count():
                    logger.info(
                        'Job posting {} has closed.'.format(page.title)
                    )
                    page.unpublish(set_expired=True)
    else:
        logger.info('No live job posting pages found...')
