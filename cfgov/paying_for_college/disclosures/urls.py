from django.urls import re_path

from paying_for_college.views import (
    BaseTemplateView, ConstantsRepresentation, ExpenseRepresentation,
    FeedbackView, OfferView, ProgramRepresentation, SchoolRepresentation,
    StatsRepresentation, VerifyView, school_autocomplete
)


app_name = "disclosures"

urlpatterns = [

    re_path(r"^offer/$", OfferView.as_view(),
            name="offer"),

    re_path(r"^offer/test/$", OfferView.as_view(), {"test": True},
            name="offer_test"),

    re_path(r"^feedback/$", FeedbackView.as_view(),
            name="pfc-feedback"),

    re_path(r"^about-this-tool/$",
            BaseTemplateView.as_view(
                template_name="paying_for_college/disclosure_technote.html"),
            name="pfc-technote"),

    re_path(
        r"^api/search-schools.json",
        school_autocomplete,
        name="school_search"),

    re_path(r"^api/program/([^/]+)/$", ProgramRepresentation.as_view(),
            name="program-json"),

    re_path(r"^api/constants/$", ConstantsRepresentation.as_view(),
            name="constants-json"),

    re_path(r"^api/national-stats/$", StatsRepresentation.as_view(),
            name="national-stats-generic-json"),

    re_path(r"^api/national-stats/(?P<id_pair>[^/]+)/$",
            StatsRepresentation.as_view(), name="national-stats-json"),

    re_path(r"^api/expenses/$", ExpenseRepresentation.as_view(),
            name="expenses-json"),

    re_path(r"^api/verify/$", VerifyView.as_view(),
            name="verify"),

    re_path(r"^api/school/(\d+)/$", SchoolRepresentation.as_view(),
            name="school-json"),
]
