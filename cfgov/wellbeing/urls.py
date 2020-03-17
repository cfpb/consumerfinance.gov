from django.views.generic import TemplateView

from wellbeing.views import ResultsView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(
        r'^$',
        TemplateView.as_view(template_name='wellbeing/home.html'),
        name='fwb_home'
    ),
    re_path(
        r'^results/$', ResultsView.as_view(), name='fwb_results'
    ),
    re_path(
        r'^about/$',
        TemplateView.as_view(template_name='wellbeing/about.html'),
        name='fwb_about'
    ),
]
