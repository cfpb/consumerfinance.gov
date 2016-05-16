from django.conf.urls import *

from django.core.context_processors import csrf
from django.conf import settings
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns(
    'jobmanager.views',
    url(r'^$', 'index', name='jobs'),
    url(r'^current-openings/$', 'current_openings', name='current_openings'),

    url(r'application-process',
        TemplateView.as_view(template_name='about-us/careers/application-process/index.html')),
    url(r'working-at-cfpb/$',
        TemplateView.as_view(template_name='about-us/careers/working-at-cfpb/index.html')),
    url(r'students-and-graduates/$',
        TemplateView.as_view(template_name='about-us/careers/students-and-graduates/index.html')),

    # Deprecated /jobs/design-technology-fellows/. Will keep it to keep the external links functioning
    url(r'^fellowship_form_submit/$', 'fellowship_form_submit', name='fellowship_form_submit'),

    url(r'^(?P<pk>\d+)/$', 'detail', name='detail-id-redirect'),
    url(r'^(?P<slug>.+?)/$', 'detail', name='detail'),
)
