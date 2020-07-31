import os

from django.core.management.base import BaseCommand

import requests


# To invoke this command from the cfgov-refresh root:
#     cfgov/manage.py trigger_jenkins_build [report_page_id]
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('report_page_id', type=int)

    def handle(self, *args, **options):
        report_id = options['report_page_id']

        jenkins_address = os.environ.get('JENKINS_API_URL')
        jenkins_user = os.environ.get('JENKINS_API_USER')
        jenkins_token = os.environ.get('JENKINS_API_TOKEN')
        job_name = os.environ.get('RESEARCH_REPORT_JENKINS_JOB')

        with requests.Session() as s:
            # Two-step authentication process. Step 1: Request crumb
            s.auth = (jenkins_user, jenkins_token)
            initial_request = f'{jenkins_address}/crumbIssuer/api/json'
            crumb_response = s.get(initial_request).json()

            # Step 2: Use crumb to make the API request
            crumb_header = crumb_response['crumbRequestField']
            crumb_value = crumb_response['crumb']
            s.post(
                f'{jenkins_address}/job/{job_name}/buildWithParameters',
                headers={crumb_header: crumb_value},
                data={'REPORT_PAGE_ID': report_id}
            )
