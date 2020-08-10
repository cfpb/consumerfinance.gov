from search.views import results_view


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(
        r"^$",
        results_view,
        # TemplateView.as_view(template_name="wellbeing/about.html")
        name="search_results",
    ),
]
