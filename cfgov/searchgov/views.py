import math

from django.conf import settings

import requests

from core.feature_flags import environment_is
from core.views import TranslatedTemplateView

from .forms import SearchForm


API_ENDPOINT = "https://api.gsa.gov/technology/searchgov/v2/results/i14y?affiliate={}&access_key={}&limit={}&offset={}&query={}"
RESULTS_PER_PAGE = 20


def get_affiliate(context):
    """Given a request, return the appropriate affiliate for Search.gov.
    Our default affiliate code is "cfpb". We have a separate Spanish-language
    index named "cfpb_es". We then have two additional indexes, "cfpb_beta"
    and "cfpb_beta_es", for use on beta.consumerfinance.gov.
    """
    affiliate = "cfpb"

    if environment_is("beta"):
        affiliate += "_beta"

    if context.get("current_language") == "es":
        affiliate += "_es"

    return affiliate


def get_api_key(context):
    if context.get("current_language") == "es":
        return settings.SEARCHGOV_ES_API_KEY
    return settings.SEARCHGOV_API_KEY


class SearchView(TranslatedTemplateView):
    template_name = "searchgov/index.html"

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = SearchForm(request.GET)
        results = []
        total_pages = 1
        current_page = 1
        count = 0
        offset = 0
        start_index = 1
        end_index = RESULTS_PER_PAGE
        query = ""
        affiliate = get_affiliate(context)
        api_key = get_api_key(context)

        if form.is_valid():
            query = form.cleaned_data["q"]
            offset = (form.cleaned_data["page"] - 1) * RESULTS_PER_PAGE
            response = requests.get(
                API_ENDPOINT.format(
                    affiliate, api_key, RESULTS_PER_PAGE, offset, query
                )
            )

            if response.status_code == 200:
                data = response.json()["web"]
                results = data["results"]
                count = data["total"]

                if count > 999:
                    count = 999

                # Protect against page shenanigans
                if offset < count:
                    total_pages = math.ceil(count / RESULTS_PER_PAGE)
                    current_page = form.cleaned_data["page"]

                    start_index = offset + 1
                    end_index = offset + RESULTS_PER_PAGE

                    if end_index > count:
                        end_index = count

                    for res in results:
                        # Strip | CFPB suffix
                        res["title"] = res["title"][:-39]
                else:
                    count = 0
        context.update(
            {
                "query": query,
                "count": count,
                "start_index": start_index,
                "end_index": end_index,
                "total_pages": total_pages,
                "current_page": current_page,
                "results": results,
            }
        )

        return self.render_to_response(context)
