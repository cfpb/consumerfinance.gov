import json
import logging
import os
import sys

import requests
from bs4 import BeautifulSoup

from jobmanager.models.pages import JobListingPage


logger = logging.getLogger(__name__)

URL = os.environ.get("USAJOBS_ARCHIVE_URL")
HEADERS = {
    "Host": os.environ.get("USAJOBS_HOST"),
    "User-Agent": os.environ.get("USAJOBS_USER"),
    "Authorization-Key": os.environ.get("USAJOBS_API_KEY"),
}
CLOSED_TEXT = "This job announcement has closed"


def job_page_closed(link):
    try:
        webpage = requests.get(link)
        soup = BeautifulSoup(webpage.text, "html.parser")
        closed_div = soup.find("div", attrs={"class": "usajobs-joa-closed"})
        return closed_div and CLOSED_TEXT in closed_div.contents
    except Exception:
        logger.exception('Check of USAJobs page "{}" failed'.format(link))
        sys.exit(1)


def job_archived(link):
    try:
        job = os.path.basename(os.path.normpath(link))
        params = {"ControlNumber": job, "WhoMayApply": "all"}
        response = requests.get(URL, headers=HEADERS, params=params, timeout=45)
        response.raise_for_status()
        response_text = json.loads(response.text)
        results = response_text["SearchResult"]
        if results["SearchResultCount"]:
            item = results["SearchResultItems"][0]
            return item["MatchedObjectId"] == job
    except Exception:
        logger.exception('API check for job "{}" failed'.format(link))
        sys.exit(1)


def is_closed(link):
    """
    USAJobs API is not currently returning results for non-public jobs, so
    we temporarily check the status of these positions on their USAJobs pages.
    """
    applicant_type = link.applicant_type.applicant_type.lower()
    if "public" in applicant_type or "citizens" in applicant_type:
        return job_archived(link.url)
    else:
        return job_page_closed(link.url)


def run():
    logger.info("Searching for live job posting pages...")
    job_pages = JobListingPage.objects.filter(live=True)
    if job_pages:
        for page in job_pages:
            logger.info('Checking status of job posting "{}"...'.format(page.title))
            if page.usajobs_application_links:
                closed_count = 0
                links = page.usajobs_application_links.all()
                for link in links:
                    if is_closed(link):
                        closed_count += 1
                if closed_count == links.count():
                    page.unpublish(set_expired=True)
                    logger.info("Job posting {} has closed.".format(page.title))
    else:
        logger.info("No live job posting pages found...")
