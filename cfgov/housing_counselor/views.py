import logging
import re

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from legacy.forms import HousingCounselorForm


logger = logging.getLogger(__name__)


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class HousingCounselorS3URLMixin(object):

    @staticmethod
    def s3_url(file_format, zipcode):
        path = settings.HOUSING_COUNSELOR_S3_PATH_TEMPLATE.format(
            file_format=file_format,
            zipcode=zipcode
        )
        return path

    @classmethod
    def s3_json_url(cls, zipcode):
        return cls.s3_url(file_format='json', zipcode=zipcode)

    @classmethod
    def s3_pdf_url(cls, zipcode):
        return cls.s3_url(file_format='pdf', zipcode=zipcode)


class HousingCounselorView(TemplateView, HousingCounselorS3URLMixin):
    template_name = 'housing_counselor/index.html'

    invalid_zip_msg = {
        'error_message': "Sorry, you have entered an invalid ZIP code.",
        'error_help': "Please enter a valid five-digit ZIP code below.",
    }

    failed_fetch_msg = {
        'error_message': "Sorry, there was an error retrieving your results.",
        'error_help': "Please try again later.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN

        zipcode = self.request.GET.get('zipcode')
        context['zipcode'] = zipcode

        if zipcode:
            zipcode_valid = re.match(r'^\d{5}$', zipcode)

            if zipcode_valid:
                try:
                    api_json = self.get_counselors(self.request, zipcode)
                except requests.HTTPError:
                    context.update(self.invalid_zip_msg)
                except requests.exceptions.ConnectionError as err:
                    logger.warning(err)
                    context.update(self.failed_fetch_msg)
                else:
                    context.update({
                        'zipcode_valid': True,
                        'api_json': api_json,
                        'pdf_url': self.s3_pdf_url(zipcode),
                    })
            else:
                context.update(self.invalid_zip_msg)

        return context

    @classmethod
    def get_counselors(cls, request, zipcode):
        """Return list of housing counselors closest to a given zipcode.

        Raises requests.HTTPError on for nonexistent ZIP code.
        Raises requests.exceptions.ConnectionError for aborted connections.
        """
        api_url = cls.s3_json_url(zipcode)

        response = requests_retry_session().get(api_url)
        response.raise_for_status()

        return response.json()


class HousingCounselorPDFView(View, HousingCounselorS3URLMixin):
    def get(self, request):
        form = HousingCounselorForm(request.GET)

        if not form.is_valid():
            return HttpResponseBadRequest('invalid zip code')

        zipcode = form.cleaned_data['zip']
        return redirect(self.s3_pdf_url(zipcode))
