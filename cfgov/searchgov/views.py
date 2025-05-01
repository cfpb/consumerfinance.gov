from django.conf import settings
from django.template.defaultfilters import title

import requests

from core.feature_flags import environment_is
from core.views import TranslatedTemplateView

from .forms import SearchForm


API_ENDPOINT = "https://api.gsa.gov/technology/searchgov/v2/results/i14y?affiliate={}&access_key={}&query={}"


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
    heading = "Search for a page"

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = SearchForm(request.GET)
        results = []
        query = ""
        affiliate = get_affiliate(context)
        api_key = get_api_key(context)

        if form.is_valid():
            query = form.cleaned_data["q"]
            response = requests.get(
                API_ENDPOINT.format(affiliate, api_key, query)
            )
            results = response.json()["web"]["results"]
            for res in results:
                # Strip | CFPB suffix
                res["title"] = res["title"][:-39]

        context.update(
            {
                "title": title(self.heading),
                "heading": self.heading,
                "query": query,
                "results": results,
            }
        )

        return self.render_to_response(context)
