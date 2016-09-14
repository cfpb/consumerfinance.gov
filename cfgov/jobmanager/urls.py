from django.conf.urls import patterns, url

from flags.views import FlaggedTemplateView
from jobmanager.views import CurrentOpeningsView, FLAG_NAME, IndexView
from transition_utilities.conditional_urls import wagtail_fail_through


urlpatterns = patterns(
    'jobmanager.views',

    url(r'^$',
        IndexView.as_view(
            flag_name=FLAG_NAME,
            fallback_view=wagtail_fail_through
        ),
        name='jobs'),
    url(r'^current-openings/$',
        CurrentOpeningsView.as_view(
            flag_name=FLAG_NAME,
            fallback_view=wagtail_fail_through
        ),
        name='current_openings'),
    url(r'application-process', FlaggedTemplateView.as_view(
        flag_name=FLAG_NAME,
        fallback_view=wagtail_fail_through,
        template_name='about-us/careers/application-process/index.html'
    )),
    url(r'working-at-cfpb/$', FlaggedTemplateView.as_view(
        flag_name=FLAG_NAME,
        fallback_view=wagtail_fail_through,
        template_name='about-us/careers/working-at-cfpb/index.html'
    )),
    url(r'students-and-graduates/$', FlaggedTemplateView.as_view(
        flag_name=FLAG_NAME,
        fallback_view=wagtail_fail_through,
        template_name='about-us/careers/students-and-graduates/index.html'
    )),

    # Deprecated /jobs/design-technology-fellows/.
    # Will keep it to keep the external links functioning.
    url(r'^fellowship_form_submit/$',
        'fellowship_form_submit',
        name='fellowship_form_submit'),

    url(r'^(?P<pk>\d+)/$', 'detail', name='detail-id-redirect'),
    url(r'^(?P<slug>.+?)/$', 'detail', name='detail'),
)
