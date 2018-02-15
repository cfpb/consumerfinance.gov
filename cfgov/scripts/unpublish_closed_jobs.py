import logging
from urllib2 import urlopen
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
    try:
        webpage = urlopen(link)
        soup = BeautifulSoup(webpage, 'html.parser')
        closed_text = soup.find('div', attrs={'class': 'usajobs-joa-closed'})
        if closed_text:
            return 'This job announcement has closed' in closed_text.contents
    except:
        logger.info('Check of USAJobs page "{}" failed'.format(link))


def job_archived(link):
    try:
        job = os.path.basename(os.path.normpath(link))
        params = {
            'ControlNumber': job,
            'WhoMayApply': 'all'
        }
        response = requests.get(URL, headers=HEADERS,
                                params=params, timeout=45)
        response.raise_for_status()
        response_text = json.loads(response.text)
        results = response_text['SearchResult']
        if results['SearchResultCount']:
            item = results['SearchResultItems'][0]
            return item['MatchedObjectId'] == job
    except requests.exceptions.HTTPError as e:
        logger.info(
            'Request for {} failed with HTTP error: "{}"'.format(job, e)
        )
    except requests.exceptions.Timeout:
        logger.info(
            'Request for {} timed out'.format(job)
        )
    except requests.exceptions.ConnectionError as e:
        logger.info(
            'Request for {} failed with connection error: "{}"'.format(job, e)
        )
    except requests.exceptions.RequestException as e:
        logger.info(
            'Request for {} failed with error: "{}"'.format(job, e)
        )
    except:
        logger.info(
            'API check for {} failed'.format(job)
        )


def run():
    logger.info('Searching for live job posting pages...')
    job_pages = JobListingPage.objects.filter(live=True)

    if job_pages:
        for page in job_pages:
            logger.info(
                'Checking status of job posting "{}"...'.format(page.title)
            )
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
