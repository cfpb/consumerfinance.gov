from django.conf.urls import url
from django.views.generic import TemplateView

from wellbeing.views import ResultsView


urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='wellbeing/home.html'),
        name='fwb_home'
    ),
    url(
        r'^results/$', ResultsView.as_view(), name='fwb_results'
    ),
    url(
        r'^about/$',
        TemplateView.as_view(template_name='wellbeing/about.html'),
        name='fwb_about'
    ),
]
