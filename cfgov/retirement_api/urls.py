from retirement_api.views import estimator

from core.views import TranslatedTemplateView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


app_name = "retirement_api"

urlpatterns = [
    re_path(
        r"^before-you-claim/about/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/about.html",
            language="en"
        ),
        name="retirement_about_en"
    ),
    re_path(
        r"^before-you-claim/about/es/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/about.html",
            language="es"
        ),
        name="retirement_about_es"
    ),
    re_path(
        r"^before-you-claim/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/claiming.html",
            language="en"
        ),
        name="claiming_en"
    ),
    re_path(
        r"^before-you-claim/es/$",
        TranslatedTemplateView.as_view(
            template_name="retirement_api/claiming-es.html",
            language="es"
        ),
        name="claiming_es"
    ),
    re_path(
        r"^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$",
        estimator,
        name="estimator",
    ),
    re_path(
        r"^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$",
        estimator,
        {"language": "es"},
        name="estimator_es",
    ),
]
