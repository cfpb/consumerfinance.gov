from core.views import TranslatedTemplateView
from retirement_api.views import estimator


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

app_name = "retirement_api_es"

urlpatterns = [
    re_path(
        r"^antes-de-solicitar/mas-sobre/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/about.html", language="es"
        ),
        name="about",
    ),
    re_path(
        r"^antes-de-solicitar/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/claiming-es.html", language="es"
        ),
        name="claiming",
    ),
    re_path(
        r"^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$",
        estimator,
        {"language": "es"},
        name="estimator",
    ),
]
