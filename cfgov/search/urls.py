from django.urls import re_path

from search.views import results_view


urlpatterns = [
    re_path(
        r"^$",
        results_view,
        # TemplateView.as_view(template_name="wellbeing/about.html")
        name="search_results",
    ),
]
