from django.conf.urls import url
from django.views.generic import TemplateView

from views import GetName


urlpatterns = [
    url(
        r'^voluntary-assessment-form/$',
        GetName.as_view(),
        name='voluntary_assessment_form'
    ),
    url(
        r'^form-submitted/$',
        TemplateView.as_view(
            template_name='diversity_inclusion/form-submitted.html'
        ),
        name='form_submitted'
    ),
]
