from django.conf.urls import url

from college.views import (
    BaseTemplateView, ConstantsRepresentation, ExpenseRepresentation,
    FeedbackView, OfferView, ProgramRepresentation, SchoolRepresentation,
    StatsRepresentation, VerifyView, school_search_api
)


urlpatterns = [

    url(r'^offer/$',
        OfferView.as_view(), name='offer'),

    url(r'^offer/test/$',
        OfferView.as_view(), {'test': True}, name='offer_test'),

    url(r'^feedback/$',
        FeedbackView.as_view(),
        name='pfc-feedback'),

    url(r'^about-this-tool/$',
        BaseTemplateView.as_view(template_name="technote.html"),
        name='pfc-technote'),

    url(r'^api/search-schools.json',
        school_search_api,
        name='school_search'),

    url(r'^api/program/([^/]+)/$',
        ProgramRepresentation.as_view(),
        name='program-json'),

    url(r'^api/constants/$',
        ConstantsRepresentation.as_view(),
        name='constants-json'),

    url(r'^api/national-stats/$',
        StatsRepresentation.as_view(),
        name='national-stats-generic-json'),

    url(r'^api/national-stats/(?P<id_pair>[^/]+)/$',
        StatsRepresentation.as_view(),
        name='national-stats-json'),

    url(r'^api/expenses/$',
        ExpenseRepresentation.as_view(),
        name='expenses-json'),

    url(r'^api/verify/$',
        VerifyView.as_view(),
        name='verify'),

    url(r'^api/school/(\d+)/$',
        SchoolRepresentation.as_view(),
        name='school-json'),
]
