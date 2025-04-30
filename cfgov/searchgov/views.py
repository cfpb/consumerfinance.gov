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
