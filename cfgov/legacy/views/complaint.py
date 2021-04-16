import logging
from datetime import datetime, timedelta

from django.views.generic import TemplateView

from complaint_search import views
from flags.state import flag_enabled
from rest_framework.test import APIRequestFactory


logger = logging.getLogger(__name__)


class ComplaintLandingView(TemplateView):
    """Consumer Complaint Database landing page view.

    This view renders the template for the CCDB landing page.

    That template includes a hardcoded value for percent of timely complaint
    responses, which is currently 97%.

    It also optionally pulls down a JSON file containing CCDB status, and uses
    the contents of that file to display a warning banner if the data is out
    of date, or if a feature flag has been set to indicate other problems.
    """
    template_name = 'complaint/complaint-landing.html'

    def get_context_data(self, **kwargs):
        context = super(ComplaintLandingView, self).get_context_data(**kwargs)

        ccdb_status_json = self.get_ccdb_status_json()
        context.update(self.is_ccdb_out_of_date(ccdb_status_json))

        context.update({
            'technical_issues': flag_enabled('CCDB_TECHNICAL_ISSUES'),
        })

        return context

    def get_ccdb_status_json(self):
        """Retrieve JSON describing the CCDB's status from a given URL."""
        try:
            args = {'field': 'all', 'size': '1', 'no_aggs': 'true'}
            factory = APIRequestFactory()
            request = factory.get('/search/', args, format='json')
            response = views.search(request)

            if response.status == 200:
                res_json = response.data
            else:
                logger.exception("Elasticsearch failed to return a valid " +
                                 "response. Response data returned: {}"
                                 .format(response.data))
                res_json = {}
        except ValueError:
            logger.exception("CCDB status data not valid JSON.")
            res_json = {}
        except Exception:
            logger.exception("CCDB status data fetch failed.")
            res_json = {}

        return res_json

    def is_ccdb_out_of_date(self, res_json):
        """Parse JSON describing CCDB status to determine if it is out of date.

        Returns a dict with two keys: data_down and narratives_down. Values
        for both of these are booleans.
        """
        data_down = flag_enabled('CCDB_TECHNICAL_ISSUES')
        narratives_down = False
        # show notification starting fifth business day data has not been
        # updated M-Th, data needs to have been updated 6 days ago; F-S,
        # preceding Monday
        now = datetime.now()
        weekday = datetime.weekday(now)
        delta = weekday if weekday > 3 else 6
        four_business_days_ago = (now -
                                  timedelta(delta)).strftime("%Y-%m-%d")

        try:
            if res_json['_meta']['last_indexed'] < four_business_days_ago:
                data_down = True
            elif (res_json['_meta']['last_updated'] <
                    four_business_days_ago):
                narratives_down = True
        except (TypeError, KeyError):
            logger.exception("CCDB JSON status not in expected format.")

        return {
            'data_down': data_down,
            'narratives_down': narratives_down,
        }
