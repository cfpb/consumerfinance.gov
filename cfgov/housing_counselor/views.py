import logging
import re

from django.conf import settings
from django.views.generic import TemplateView

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


logger = logging.getLogger(__name__)

S3_PATH_TEMPLATE = "https://{bucket_location}/a/assets/hud/{file_format}s/{zipcode}.{file_format}"


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
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class HousingCounselorS3URLMixin:
    @classmethod
    def s3_json_url(cls, zipcode):
        return S3_PATH_TEMPLATE.format(
            bucket_location=f"s3.amazonaws.com/{settings.AWS_STORAGE_BUCKET_NAME}",
            file_format="json",
            zipcode=zipcode,
        )

    @classmethod
    def s3_pdf_url(cls, zipcode):
        return S3_PATH_TEMPLATE.format(
            bucket_location=settings.AWS_S3_CUSTOM_DOMAIN,
            file_format="pdf",
            zipcode=zipcode,
        )


class HousingCounselorView(TemplateView, HousingCounselorS3URLMixin):
    template_name = "housing_counselor/index.html"

    invalid_zip_msg = {
        "invalid_zip_error_message": "You must enter a valid 5-digit ZIP \
            code.",
    }

    failed_fetch_msg = {
        "failed_fetch_error_message": "There was a problem retrieving \
            your results",
        "failed_fetch_error_explanation": "Please try again later.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mapbox_access_token"] = settings.MAPBOX_ACCESS_TOKEN

        zipcode = self.request.GET.get("zipcode")
        context["zipcode"] = zipcode

        if zipcode:
            zipcode_valid = re.match(r"^\d{5}$", zipcode)

            if zipcode_valid:
                try:
                    api_json = self.get_counselors(self.request, zipcode)
                except requests.HTTPError:
                    context.update(self.invalid_zip_msg)
                except requests.exceptions.ConnectionError as err:
                    logger.warning(err)
                    context.update(self.failed_fetch_msg)
                else:
                    context.update(
                        {
                            "zipcode_valid": True,
                            "api_json": api_json,
                            "pdf_url": self.s3_pdf_url(zipcode),
                        }
                    )
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
