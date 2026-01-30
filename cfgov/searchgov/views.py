import math
from base64 import b32decode
from binascii import Error
from html import unescape
from urllib.parse import urlencode

from django.conf import settings
from django.http import JsonResponse

import requests

from core.views import TranslatedTemplateView

from .forms import SearchForm


# Search.gov API docs: https://open.gsa.gov/api/searchgov-results/
API_ENDPOINT = "https://api.gsa.gov/technology/searchgov/v2/results/i14y?{}"
RESULTS_PER_PAGE = 20


def get_affiliate(context):
    """Given a request, return the appropriate affiliate for Search.gov.
    Our default affiliate code is "cfpb". We have a separate Spanish-language
    index named "cfpb_es".
    """
    if context.get("current_language") == "es":
        return "cfpb_es"

    return "cfpb"


def get_api_key(context):
    if context.get("current_language") == "es":
        return settings.SEARCHGOV_ES_API_KEY
    return settings.SEARCHGOV_API_KEY


def encode_url(params):
    return API_ENDPOINT.format(urlencode(params))


def recreate_unencoded(parts):
    return ", ".join(parts).capitalize()


def decode_meta(encoded):
    return unescape(b32decode(encoded.upper()).decode("utf-8"))


class SearchView(TranslatedTemplateView):
    template_name = "searchgov/index.html"

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = SearchForm(request.GET)
        results = []
        recommended = []
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
                encode_url(
                    {
                        "include_facets": "true",
                        "affiliate": affiliate,
                        "access_key": api_key,
                        "limit": RESULTS_PER_PAGE,
                        "offset": offset,
                        "query": query,
                    }
                )
            )

            if response.status_code == 200:
                json_data = response.json()
                data = json_data["web"]
                results = data["results"]
                recommended = json_data["text_best_bets"]
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

                    # Post proprocess results
                    for res in results:
                        # Strip | CFPB suffix
                        encoded_list = res.get("searchgov_custom2")
                        if encoded_list:
                            # Hack due to search.gov caching old data
                            try:
                                res["description"] = decode_meta(
                                    encoded_list[0]
                                )
                            # binascii Error points to likely unencoded data
                            except Error:
                                res["description"] = recreate_unencoded(
                                    encoded_list
                                )
                        else:
                            res["description"] = res["snippet"]

                else:
                    count = 0

        context_data = {
            "query": query,
            "count": count,
            "start_index": start_index,
            "end_index": end_index,
            "total_pages": total_pages,
            "current_page": current_page,
            "recommended": recommended,
            "results": results,
        }

        if form.cleaned_data.get("format") == "json":
            return JsonResponse(context_data)

        context.update(context_data)

        return self.render_to_response(context)
