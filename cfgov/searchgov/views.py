from django.conf import settings
from django.template.defaultfilters import title

import requests

from core.views import TranslatedTemplateView

from .forms import SearchForm


API_ENDPOINT = f"https://api.gsa.gov/technology/searchgov/v2/results/i14y?affiliate=cfpb&access_key={settings.SEARCHGOV_API_KEY}&query="


class SearchView(TranslatedTemplateView):
    template_name = "searchgov/index.html"
    heading = "Search for a page"

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
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

        context.update(
            {
                "title": title(self.heading),
                "heading": self.heading,
                "query": query,
                "results": results,
            }
        )

        return self.render_to_response(context)
