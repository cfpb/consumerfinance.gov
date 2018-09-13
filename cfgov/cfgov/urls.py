from functools import partial

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import render
from django.views.defaults import page_not_found
from django.views.generic.base import RedirectView, TemplateView

from wagtail.contrib.wagtailsitemaps.views import sitemap
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtailsharing import urls as wagtailsharing_urls
from wagtailsharing.views import ServeView

from flags.urls import flagged_url
from flags.views import FlaggedTemplateView

from ask_cfpb.views import (
    ask_autocomplete, ask_search, print_answer, redirect_ask_search,
    view_answer
)
from core.views import (
    ExternalURLNoticeView, govdelivery_subscribe, regsgov_comment
)
from legacy.views import token_provider
from legacy.views.complaint import ComplaintLandingView
from legacy.views.housing_counselor import (
    HousingCounselorPDFView, HousingCounselorView
)
from regulations3k.views import redirect_eregs
from transition_utilities.conditional_urls import include_if_app_enabled
from v1.auth_forms import CFGOVPasswordChangeForm
from v1.views import (
    change_password, check_permissions, login_with_lockout,
    password_reset_confirm, welcome
)
from v1.views.documents import DocumentServeView


def flagged_wagtail_template_view(flag_name, template_name):
    """View that serves Wagtail if a flag is set, and a template if not.

    This uses the wagtail-sharing ServeView to ensure that sharing works
    properly when viewing the page in Wagtail behind a flag.
    """
    return FlaggedTemplateView.as_view(
        fallback=lambda request: ServeView.as_view()(request, request.path),
        flag_name=flag_name,
        template_name=template_name,
        condition=False
    )


def flagged_wagtail_only_view(flag_name, regex_path, url_name=None):
    """ Teachers Digital Platform static pages are very similar so
    in the name of DRY we are implementing them with this method.
    """
    return flagged_url(
        flag_name,
        regex_path,
        lambda request: ServeView.as_view()(request, request.path),
        fallback=page_not_found,
        name=url_name,
    )


urlpatterns = [
    url(r'^documents/(?P<document_id>\d+)/(?P<document_filename>.*)$',
        DocumentServeView.as_view(),
        name='wagtaildocs_serve'),

    url(r'^home/(?P<path>.*)$',
        RedirectView.as_view(url='/%(path)s', permanent=True)),

    url(r'^owning-a-home/static/(?P<path>.*)$',
        RedirectView.as_view(
            url='/static/owning-a-home/static/%(path)s', permanent=True)),
    url(r'^owning-a-home/resources/(?P<path>.*)$',
        RedirectView.as_view(
            url='/static/owning-a-home/resources/%(path)s', permanent=True)),
    url(r'^owning-a-home/closing-disclosure/$',
        TemplateView.as_view(
            template_name='owning-a-home/closing-disclosure/index.html'),
            name='closing-disclosure'
    ),
    url(r'^owning-a-home/explore-rates/',
        TemplateView.as_view(
            template_name='owning-a-home/explore-rates/index.html'),
            name='explore-rates'
    ),
    url(r'^owning-a-home/loan-estimate/$',
        TemplateView.as_view(
            template_name='owning-a-home/loan-estimate/index.html'),
            name='loan-estimate'
    ),

    # Temporarily serve Wagtail OAH journey pages at `/process/` urls.
    # TODO: change to redirects after 2018 homebuying campaign.
    url(r'^owning-a-home/process/(?P<path>.*)$',
        lambda req, path: ServeView.as_view()(
            req, 'owning-a-home/{}'.format(path or 'prepare/')
        ),
    ),
    # END TODO

    url(r'^know-before-you-owe/$',
        TemplateView.as_view(
        template_name='know-before-you-owe/index.html'),
        name='know-before-you-owe'),
    url(r'^know-before-you-owe/timeline/$',
        TemplateView.as_view(
        template_name='know-before-you-owe/timeline/index.html'),
        name='kbyo-timeline'),
    url(r'^know-before-you-owe/compare/$',
        TemplateView.as_view(
        template_name='know-before-you-owe/compare/index.html'),
        name='kbyo-compare'),
    url(r'^fin-ed/privacy-act-statement/$',
        TemplateView.as_view(
        template_name='/adult-financial-education/'
                      'privacy-act-statement/index.html')),
    url(r'^your-story/$', TemplateView.as_view(
        template_name='/your-story/index.html')),
    url(r'^fair-lending/$', TemplateView.as_view(
        template_name='fair-lending/index.html'),
        name='fair-lending'),

    url(r'^practitioner-resources/students/$', TemplateView.as_view(
        template_name='students/index.html'),
        name='students'),
    url(r'^practitioner-resources/students/knowbeforeyouowe/$',
        TemplateView.as_view(
            template_name='students/knowbeforeyouowe/index.html'),
            name='students-knowbeforeyouowe'),
    url(r'^practitioner-resources/students/'
         'helping-borrowers-find-ways-to-stay-afloat/$',
            TemplateView.as_view(
                template_name='students/helping-borrowers-find-'
                              'ways-to-stay-afloat/index.html'),
                name='students-helping-borrowers'),

    url(r'^parents/(?P<path>.*)$',
        RedirectView.as_view(
            url='/money-as-you-grow/%(path)s', permanent=True)),
    url(r'^blog/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/blog/%(path)s', permanent=True)),
    url(r'^newsroom/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/newsroom/%(path)s', permanent=True)),

    url(r'^the-bureau/(?P<path>.*)$',
            RedirectView.as_view(url='/about-us/the-bureau/%(path)s',
                                 permanent=True)
    ),
    url(r'^about-us/leadership-calendar/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/the-bureau/leadership-calendar/%(path)s',
        permanent=True)),

    url(r'^doing-business-with-us/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/doing-business-with-us/%(path)s', permanent=True)),

    url(r'^external-site/$', ExternalURLNoticeView.as_view(),
        name='external-site'),

    url(r'^subscriptions/new/$', govdelivery_subscribe, name='govdelivery'),

    url(r'^govdelivery-subscribe/', include([
        url(r'^success/$',
            TemplateView.as_view(
                template_name='govdelivery-subscribe/success/index.html'),
            name='success'),
        url(r'^error/$',
            TemplateView.as_view(
                template_name='govdelivery-subscribe/error/index.html'),
            name='user_error'),
        url(r'^server-error/$',
            TemplateView.as_view(
                template_name='govdelivery-subscribe/server-error/index.html'),
            name='server_error')],
        namespace='govdelivery')),

    url(r'^regulation-comment/new/$', regsgov_comment, name='reg_comment'),

    url(r'^regulation-comment/', include([
        url(r'^success/$',
            TemplateView.as_view(
                template_name='regulation-comment/success/index.html'),
            # 'core.views.comment_success',
            name='success'),
        url(r'^error/$',
            TemplateView.as_view(
                template_name='regulation-comment/error/index.html'),
            name='user_error'),
        url(r'^server-error/$',
            TemplateView.as_view(
                template_name='regulation-comment/server-error/index.html'),
            name='server_error')],
        namespace='reg_comment')),

    url(r'^feed/$',
        RedirectView.as_view(url='/about-us/blog/feed/', permanent=True)),
    url(r'^feed/blog/$',
        RedirectView.as_view(url='/about-us/blog/feed/', permanent=True)),
    url(r'^feed/newsroom/$',
        RedirectView.as_view(url='/about-us/newsroom/feed/', permanent=True)),
    url(r'^newsroom-feed/$',
        RedirectView.as_view(url='/about-us/newsroom/feed/', permanent=True)),

    url(r'^careers/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/careers/%(path)s', permanent=True)),

    url(r'^transcripts/', include([
        url(r'^how-to-apply-for-a-federal-job-with-the-cfpb/$',
            TemplateView.as_view(
                template_name='transcripts/how-to-apply-for-a-federal-job-with-the-cfpb/index.html'),  # noqa: E501
                name='how-to-apply-for-a-federal-job-with-the-cfpb'), ],
        namespace='transcripts')),
    url(r'^paying-for-college/',
        include_if_app_enabled('comparisontool', 'comparisontool.urls')),
    url(r'^paying-for-college2/',
        include_if_app_enabled(
            'paying_for_college', 'paying_for_college.config.urls')),
    url(r'^credit-cards/agreements/',
        include('agreements.urls')),

    url(r'^consumer-tools/retirement/', include_if_app_enabled(
        'retirement_api',
        'retirement_api.urls',
        namespace='retirement_api'
    )),

    url(r'^data-research/consumer-complaints/$',
        ComplaintLandingView.as_view(),
        name='complaint-landing'),

    # CCDB5-API
    flagged_url('CCDB5_RELEASE',
                r'^data-research/consumer-complaints/search/api/v1/',
                include_if_app_enabled('complaint_search',
                                       'complaint_search.urls')
                ),
    # If 'CCDB5_RELEASE' is True, include CCDB5 urls.
    flagged_url('CCDB5_RELEASE',
                r'^data-research/consumer-complaints/search/',
                include_if_app_enabled(
                    'ccdb5_ui', 'ccdb5_ui.config.urls'
                )),

    url(r'^oah-api/rates/',
        include_if_app_enabled('ratechecker', 'ratechecker.urls')),
    url(r'^oah-api/county/',
        include_if_app_enabled('countylimits', 'countylimits.urls')),

    url(r'^find-a-housing-counselor/$',
        HousingCounselorView.as_view(),
        name='housing-counselor'),
    url(r'^save-hud-counselors-list/$',
        HousingCounselorPDFView.as_view(),
        name='housing-counselor-pdf'),

    # Report redirects
    url(r'^reports/(?P<path>.*)$',
        RedirectView.as_view(
            url='/data-research/research-reports/%(path)s', permanent=True)),
    url(r'^jobs/supervision/$',
        TemplateView.as_view(
            template_name='jobmanager/supervision.html'),
        name='jobs_supervision'),

    url(r'^jobs/technology-innovation-fellows/$',
        TemplateView.as_view(
            template_name='jobmanager/technology-innovation-fellows.html'),
        name='technology_innovation_fellows'),

    # credit cards KBYO

    url(r'^credit-cards/knowbeforeyouowe/$', TemplateView.as_view(
        template_name='knowbeforeyouowe/creditcards/tool.html'),
        name='cckbyo'),
    # Form csrf token provider for JS form submission
    url(r'^token-provider/', token_provider, name='csrf-token-provider'),

    # data-research-api
    url(r'^data-research/mortgages/api/v1/',
        include_if_app_enabled('data_research', 'data_research.urls')),

    # educational resources
    url(r'^educational-resources/(?P<path>.*)$', RedirectView.as_view(
        url='/practitioner-resources/%(path)s', permanent=True)),
    url(r'^practitioner-resources/resources-for-older-adults' +
         '/managing-someone-elses-money/(?P<path>.*)$',
            RedirectView.as_view(
                url='/consumer-tools/managing-someone-elses-money/%(path)s',
                permanent=True)),
    url(r'^practitioner-resources/money-as-you-grow/(?P<path>.*)$',
            RedirectView.as_view(
                url='/consumer-tools/money-as-you-grow/%(path)s',
                permanent=True)),

    # retirement redirects
    url(r'^retirement/(?P<path>.*)$', RedirectView.as_view(
            url='/consumer-tools/retirement/%(path)s',
            permanent=True)),

    # empowerment redirects
    url(r'^empowerment/$', RedirectView.as_view(
            url='/practitioner-resources/economically-vulnerable/',
            permanent=True)),

    # students redirects
    url(r'^students/(?P<path>.*)$', RedirectView.as_view(
            url='/practitioner-resources/students/%(path)s',
            permanent=True)),

    # ask-cfpb
    url(r'^askcfpb/$',
        RedirectView.as_view(
            url='/ask-cfpb/',
            permanent=True)),
    url(r'^(?P<language>es)/obtener-respuestas/c/(.+)/(?P<ask_id>\d+)/(.+)\.html$',  # noqa: E501
         RedirectView.as_view(
             url='/es/obtener-respuestas/slug-es-%(ask_id)s',
             permanent=True)),
    url(r'^askcfpb/(?P<ask_id>\d+)/(.*)$',
         RedirectView.as_view(
             url='/ask-cfpb/slug-en-%(ask_id)s',
             permanent=True)),
    url(r'^askcfpb/search/',
        redirect_ask_search,
        name='redirect-ask-search'),
    url(r'^(?P<language>es)/obtener-respuestas/buscar/$',
        ask_search,
        name='ask-search-es'),
    url(r'^(?P<language>es)/obtener-respuestas/buscar/(?P<as_json>json)/$',
        ask_search,
        name='ask-search-es-json'),
    url(r'^(?i)ask-cfpb/([-\w]{1,244})-(en)-(\d{1,6})/$',
        view_answer,
        name='ask-english-answer'),
    url(r'^es/obtener-respuestas/([-\w]{1,244})-(es)-(\d{1,6})/$',
        view_answer,
        name='ask-spanish-answer'),
    url(r'^es/obtener-respuestas/([-\w]{1,244})-(es)-(\d{1,6})/imprimir/$',
        print_answer,
        name='ask-spanish-print-answer'),
    url(r'^(?i)ask-cfpb/search/$',
        ask_search,
        name='ask-search-en'),
    url(r'^(?i)ask-cfpb/search/(?P<as_json>json)/$',
        ask_search,
        name='ask-search-en-json'),
    url(r'^(?i)ask-cfpb/api/autocomplete/$',
        ask_autocomplete, name='ask-autocomplete-en'),
    url(r'^(?P<language>es)/obtener-respuestas/api/autocomplete/$',
        ask_autocomplete, name='ask-autocomplete-es'),

    url(r'^es/$', TemplateView.as_view(
                 template_name='/es/index.html')),

    url(r'^es/comprar-casa/$', TemplateView.as_view(
                 template_name='es/comprar-casa/index.html')),

    url(r'^es/nuestra-historia/$', TemplateView.as_view(
                 template_name='es/nuestra-historia/index.html')),

    url(r'^es/presentar-una-queja/$', TemplateView.as_view(
                 template_name='es/presentar-una-queja/index.html')),

    url(r'^es/quienes-somos/$', TemplateView.as_view(
                 template_name='es/quienes-somos/index.html')),

    url(r'^_status/', include_if_app_enabled('watchman', 'watchman.urls')),

    url(
        r'^(?i)consumer-tools/financial-well-being/',
        include('wellbeing.urls')
    ),

    url('^sitemap\.xml$', sitemap),

    flagged_url('SEARCH_DOTGOV_API',
                r'^search/',
                include('search.urls')),

    flagged_wagtail_only_view(
        'TDP_SEARCH_INTERFACE',
        r'^practitioner-resources/youth-financial-education/teach/activities/',
        'tdp_search'),

    flagged_wagtail_only_view(
        'TDP_STATIC_PAGE',
        r'^practitioner-resources/youth-financial-education/teach/'),

    flagged_wagtail_only_view(
        'TDP_STATIC_PAGE',
        r'^practitioner-resources/youth-financial-education/learn/'),

    flagged_wagtail_only_view(
        'TDP_STATIC_PAGE',
        r'practitioner-resources/youth-financial-education2/'),

    flagged_wagtail_only_view(
        'TDP_STATIC_PAGE',
        r'^practitioner-resources/youth-financial-education/glossary-financial-terms/'),  # noqa: E501

    flagged_wagtail_only_view(
        'TDP_STATIC_PAGE',
        r'^practitioner-resources/youth-financial-education/resources-research/'),  # noqa: E501

    flagged_url('TDP_CRTOOL',
        r'^practitioner-resources/youth-financial-education/curriculum-review/tool/',  # noqa: E501
        include_if_app_enabled('teachers_digital_platform',
                               'teachers_digital_platform.tool_urls')),

    flagged_url('TDP_CRTOOL',
        r'^practitioner-resources/youth-financial-education/curriculum-review/before-you-begin/',  # noqa: E501
        include_if_app_enabled('teachers_digital_platform',
                                'teachers_digital_platform.begin_urls')),

    flagged_wagtail_only_view(
        'TDP_CRTOOL',
        r'^practitioner-resources/youth-financial-education/curriculum-review/$'),  # noqa: E501

    flagged_url('TDP_BB_TOOL',
        r'^practitioner-resources/youth-financial-education/tour',  # noqa: E501
        include_if_app_enabled('teachers_digital_platform',
                                    'teachers_digital_platform.bb_urls')),

    flagged_url(
        'REGULATIONS3K',
        r'^policy-compliance/rulemaking/regulations/',
        lambda request: ServeView.as_view()(request, request.path),
        fallback=page_not_found,
        name='regulations'
    ),
    flagged_url(
        'REGULATIONS3K',
        r'^regulations3k-service-worker.js',
        TemplateView.as_view(
        template_name='regulations3k/regulations3k-service-worker.js',
        content_type='application/javascript'),
        name='regulations3k-service-worker.js'
    ),

    # Include eRegulations URLs only if the REGULATIONS3K flag state is False
    flagged_url(
        'REGULATIONS3K',
        r'^eregs-api/.*',
        include_if_app_enabled('regcore', 'regcore.urls'),
        fallback=page_not_found,
        state=False
    ),
    flagged_url(
        'REGULATIONS3K',
        r'^eregulations/.*',
        include_if_app_enabled('regulations', 'regulations.urls'),
        fallback=redirect_eregs,
        name='eregs-redirect',
        state=False
    ),

]

if settings.ALLOW_ADMIN_URL:
    patterns = [
        url(r'^login/$', login_with_lockout, name='cfpb_login'),
        url(r'^login/check_permissions/$',
            check_permissions,
            name='check_permissions'),
        url(r'^login/welcome/$', welcome, name='welcome'),
        url(r'^logout/$', auth_views.logout),
        url('^admin/login/$',
            RedirectView.as_view(url='/login/',
                                 permanent=True,
                                 query_string=True)),
        url('^django-admin/login/$',
            RedirectView.as_view(url='/login/',
                                 permanent=True,
                                 query_string=True)),

        url(r'^d/admin/(?P<path>.*)$',
            RedirectView.as_view(url='/django-admin/%(path)s',
                                 permanent=True)),

        url(r'^tasks/(?P<path>.*)$',
            RedirectView.as_view(url='/admin/cdn/%(path)s', permanent=True)),

        url(r'^django-admin/password_change',
            change_password,
            name='django_admin_account_change_password'),
        url(r'^django-admin/', include(admin.site.urls)),

        # Override Django and Wagtail password views with our password policy
        url(r'^admin/password_reset/', include([
            url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa: E501
                password_reset_confirm,
                name='password_reset_confirm')
        ])),
        url(r'^django-admin/password_change',
            auth_views.password_change,
            {'password_change_form': CFGOVPasswordChangeForm}),
        url(r'^password/change/done/$',
            auth_views.password_change_done,
            name='password_change_done'),
        url(r'^admin/account/change_password/$',
            change_password,
            name='wagtailadmin_account_change_password'),
        url(r'^admin/', include(wagtailadmin_urls)),

    ]

    urlpatterns = patterns + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # enable local preview of error pages
    urlpatterns.append(
        url(r'^500/$',
            TemplateView.as_view(template_name='500.html'),
            name='500')
    )
    urlpatterns.append(
        url(r'^404/$',
            TemplateView.as_view(template_name='404.html'),
            name='404')
    )

    try:
        import debug_toolbar
        urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass

# Catch remaining URL patterns that did not match a route thus far.
urlpatterns.append(url(r'', include(wagtailsharing_urls)))
# urlpatterns.append(url(r'', include(wagtailsharing_urls)))


def handle_error(code, request):
    try:
        return render(request, '%s.html' % code, context={'request': request},
                      status=code)
    except AttributeError:
        # for certain URL's, it seems like our middleware doesn't run
        # Thankfully, these are probably not errors real users see -- usually
        # the results of a security scan, or a malformed static file reference.

        return HttpResponse("This request could not be processed, "
                            "HTTP Error %s." % str(code), status=code)


handler404 = partial(handle_error, 404)
handler500 = partial(handle_error, 500)
