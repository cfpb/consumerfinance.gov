from django.conf import settings
from django.template.defaultfilters import title
from django.views.generic import TemplateView

import requests

from .forms import SearchForm


API_ENDPOINT = f"https://api.gsa.gov/technology/searchgov/v2/results/i14y?affiliate=cfpb&access_key={settings.SEARCHGOV_API_KEY}&query="


class SearchView(TemplateView):
    template_name = "searchgov/index.html"
    heading = "Search for a page"

    def get(self, request):
        form = SearchForm(request.GET)
        query = ""
        results = []
        if form.is_valid():
            query = form.cleaned_data["q"]
            response = requests.get(f"{API_ENDPOINT}{query}")
            results = response.json()["web"]["results"]
            for res in results:
                # Strip | CFPB suffix
                res["title"] = res["title"][:-39]

        return self.render_to_response(
            {
                "title": title(self.heading),
                "heading": self.heading,
                "query": query,
                "results": results,
            }
        )


# def api(request, dob=None, income=None, language="en"):
#    ssa_params = {
#        "dobmon": 0,
#        "dobday": 0,
#        "yob": 0,
#        "earnings": 0,
#        "lastYearEarn": "",  # not using
#        "lastEarn": "",  # not using
#        "retiremonth": "",  # only using for past-FRA users
#        "retireyear": "",  # only using for past-FRA users
#        "dollars": 1,  # benefits to be calculated in current-year dollars
#        "prgf": 2,
#    }
#    if dob is None:
#        dob = param_check(request, "dob")
#        if not dob:
#            return HttpResponseBadRequest("invalid date of birth")
#    if income is None:
#        income_raw = param_check(request, "income")
#        if not income_raw:
#            return HttpResponseBadRequest("invalid income")
#        else:
#            income = income_check(income_raw)
#            if income is None:
#                return HttpResponseBadRequest("invalid income")
#    else:
#        income = income_check(income)
#        if income is None:
#            return HttpResponseBadRequest("invalid income")
#    try:
#        dob_parsed = parser.parse(dob)
#    except ValueError:
#        return HttpResponseBadRequest("invalid date of birth")
#    else:
#        DOB = dob_parsed.date()
#    ssa_params["dobmon"] = DOB.month
#    ssa_params["dobday"] = DOB.day
#    ssa_params["yob"] = DOB.year
#    ssa_params["earnings"] = income
#    data = get_retire_data(ssa_params, language)
#    return HttpResponse(json.dumps(data), content_type="application/json")
