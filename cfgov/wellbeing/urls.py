from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='wellbeing/home.html')
    ),
    url(
        r'^results/$',
        TemplateView.as_view(template_name='wellbeing/results.html')
    ),
    url(
        r'^results-alt/$',
        TemplateView.as_view(template_name='wellbeing/results-alt.html')
    ),
    url(
        r'^compare/$',
        TemplateView.as_view(template_name='wellbeing/compare.html')
    ),
    url(
        r'^about/$',
        TemplateView.as_view(template_name='wellbeing/about.html')
    ),
]
