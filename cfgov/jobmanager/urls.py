from django.conf.urls import url

from flags.decorators import flag_required
from flags.views import FlaggedTemplateView
from jobmanager.views import (
    CurrentOpeningsView, IndexView, detail, fellowship_form_submit
)
from transition_utilities.conditional_urls import wagtail_fail_through


FLAG_NAME = 'WAGTAIL_CAREERS'


flag_kwargs = {
    'flag_name': FLAG_NAME,
    'fallback_view': wagtail_fail_through,
    'pass_if_set': False,
}


urlpatterns = [
    url(r'^$', IndexView.as_view(**flag_kwargs), name='jobs'),
    url(r'^current-openings/$',
        CurrentOpeningsView.as_view(**flag_kwargs),
        name='current_openings'),
    url(r'application-process', FlaggedTemplateView.as_view(
        template_name='about-us/careers/application-process/index.html',
        **flag_kwargs
    )),
    url(r'working-at-cfpb/$', FlaggedTemplateView.as_view(
        template_name='about-us/careers/working-at-cfpb/index.html',
        **flag_kwargs
    )),
    url(r'students-and-graduates/$', FlaggedTemplateView.as_view(
        template_name='about-us/careers/students-and-graduates/index.html',
        **flag_kwargs
    )),

    # Deprecated /jobs/design-technology-fellows/.
    # Will keep it to keep the external links functioning.
    url(r'^fellowship_form_submit/$',
        fellowship_form_submit,
        name='fellowship_form_submit'),

    url(r'^(?P<pk>\d+)/$',
        flag_required(**flag_kwargs)(detail),
        name='detail-id-redirect'),
    url(r'^(?P<slug>.+?)/$',
        flag_required(**flag_kwargs)(detail),
        name='detail'),
]
