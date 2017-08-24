from functools import partial

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import RedirectView, TemplateView
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtailsharing import urls as wagtailsharing_urls
from wagtailsharing.views import ServeView

from flags.urls import flagged_url

from ask_cfpb.views import (
    ask_search,
    ask_autocomplete,
    print_answer,
    redirect_ask_search,
    view_answer
)
from core.views import ExternalURLNoticeView
from legacy.views import token_provider
from legacy.views.housing_counselor import (
    HousingCounselorView, HousingCounselorPDFView
)
from sheerlike.sites import SheerSite
from sheerlike.views.generic import SheerTemplateView
from transition_utilities.conditional_urls import include_if_app_enabled
from v1.auth_forms import CFGOVPasswordChangeForm
from v1.views import (
    change_password,
    check_permissions,
    login_with_lockout,
    password_reset_confirm,
    welcome)
from v1.views.documents import DocumentServeView


fin_ed = SheerSite('fin-ed-resources')
oah = SheerSite('owning-a-home')
es_conv_flag = partial(flagged_url, 'ES_CONV_FLAG')

urlpatterns = [

    url(r'^documents/(?P<document_id>\d+)/(?P<document_filename>.*)$',
        DocumentServeView.as_view(),
        name='wagtaildocs_serve'),

    # TODO: Enable search route when search is available.
    # url(r'^search/$', 'search.views.search', name='search'),

    url(r'^home/(?P<path>.*)$',
        RedirectView.as_view(url='/%(path)s', permanent=True)),

    url(r'^owning-a-home/static/(?P<path>.*)$',
        RedirectView.as_view(
            url='/static/owning-a-home/static/%(path)s', permanent=True)),
    url(r'^owning-a-home/resources/(?P<path>.*)$',
        RedirectView.as_view(
            url='/static/owning-a-home/resources/%(path)s', permanent=True)),

    url(r'^owning-a-home/closing-disclosure/',
        include(oah.urls_for_prefix('closing-disclosure'))),
    url(r'^owning-a-home/explore-rates/',
        include(oah.urls_for_prefix('explore-rates'))),
    url(r'^owning-a-home/loan-estimate/',
        include(oah.urls_for_prefix('loan-estimate'))),

    url(r'^owning-a-home/loan-options/',
        include(oah.urls_for_prefix('loan-options'))),
    url(r'^owning-a-home/loan-options/FHA-loans/',
        include(oah.urls_for_prefix('loan-options/FHA-loans/'))),
    url(r'^owning-a-home/loan-options/conventional-loans/',
        include(oah.urls_for_prefix('loan-options/conventional-loans/'))),
    url(r'^owning-a-home/loan-options/special-loan-programs/',
        include(oah.urls_for_prefix('loan-options/special-loan-programs/'))),

    url(r'^owning-a-home/mortgage-closing/',
        include(oah.urls_for_prefix('mortgage-closing'))),
    url(r'^owning-a-home/mortgage-estimate/',
        include(oah.urls_for_prefix('mortgage-estimate'))),

    url(r'^owning-a-home/process/',
        include(oah.urls_for_prefix('process/prepare/'))),
    url(r'^owning-a-home/process/prepare/',
        include(oah.urls_for_prefix('process/prepare/'))),
    url(r'^owning-a-home/process/explore/',
        include(oah.urls_for_prefix('process/explore/'))),
    url(r'^owning-a-home/process/compare/',
        include(oah.urls_for_prefix('process/compare/'))),
    url(r'^owning-a-home/process/close/',
        include(oah.urls_for_prefix('process/close/'))),
    url(r'^owning-a-home/process/sources/',
        include(oah.urls_for_prefix('process/sources/'))),

    # the redirect is an unfortunate workaround, could be resolved by
    # using static('path/to/asset') in the source template
    url(r'^know-before-you-owe/static/(?P<path>.*)$',
        RedirectView.as_view(
            url='/static/know-before-you-owe/static/%(path)s',
            permanent=True)),
    url(r'^know-before-you-owe/',
        include(SheerSite('know-before-you-owe').urls)),

    url(r'^adult-financial-education/',
        include(fin_ed.urls_for_prefix('adult-financial-education'))),
    url(r'^your-story/$', TemplateView.as_view(
        template_name='/your-story/index.html')),
    url(r'^parents/(?P<path>.*)$',
        RedirectView.as_view(
            url='/money-as-you-grow/%(path)s', permanent=True)),
    url(r'fin-ed/privacy-act-statement/',
        include(fin_ed.urls_for_prefix('privacy-act-statement'))),
    url(r'^blog/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/blog/%(path)s', permanent=True)),
    url(r'^newsroom/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/newsroom/%(path)s', permanent=True)),

    flagged_url(
        'WAGTAIL_ABOUT_US',
        r'^about-us/newsroom/press-resources/$',
        lambda req: ServeView.as_view()(req, req.path),
        fallback=TemplateView.as_view(
            template_name='newsroom/press-resources/index.html'),
        name='press-resources'),

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
    url(r'^about-us/doing-business-with-us/', include([
        flagged_url(
            'WAGTAIL_DOING_BUSINESS_WITH_US',
            r'^$',
            lambda req: ServeView.as_view()(req, req.path),
            fallback=TemplateView.as_view(
                template_name='about-us/doing-business-with-us/index.html'),
            name='index'),
        flagged_url(
            'WAGTAIL_DOING_BUSINESS_WITH_US',
            r'^(?P<page_slug>[\w-]+)/$',
            lambda req, page_slug: ServeView.as_view()(req, req.path),
            fallback=SheerTemplateView.as_view(),
            name='page')
        ],
        namespace='business')),

    url(r'^external-site/$', ExternalURLNoticeView.as_view(),
        name='external-site'),

    url(r'^subscriptions/new/$',
        'core.views.govdelivery_subscribe',
        name='govdelivery'),

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

    url(r'^regulation-comment/new/$',
        'core.views.regsgov_comment',
        name='reg_comment'),

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

    # Testing reg comment form
    url(r'^reg-comment-form-test/$',
        SheerTemplateView.as_view(
            template_name='regulation-comment/reg-comment-form-test.html'),
        name='reg-comment-form-test'),

    url(r'^feed/$',
        RedirectView.as_view(url='/about-us/blog/feed/', permanent=True)),
    url(r'^feed/blog/$',
        RedirectView.as_view(url='/about-us/blog/feed/', permanent=True)),
    url(r'^feed/newsroom/$',
        RedirectView.as_view(url='/about-us/newsroom/feed/', permanent=True)),
    url(r'^newsroom-feed/$',
        RedirectView.as_view(url='/about-us/newsroom/feed/', permanent=True)),

    flagged_url(
        'WAGTAIL_ABOUT_US',
        r'^about-us/$',
        lambda req: ServeView.as_view()(req, req.path),
        fallback=SheerTemplateView.as_view(
            template_name='about-us/index.html'),
        name='about-us'),

    url(r'^careers/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/careers/%(path)s', permanent=True)),

    url(r'^transcripts/', include([
        url(r'^how-to-apply-for-a-federal-job-with-the-cfpb/$',
            SheerTemplateView.as_view(
                template_name='transcripts/how-to-apply-for-a-federal-job-with-the-cfpb/index.html'),  # noqa: E501
                name='how-to-apply-for-a-federal-job-with-the-cfpb'), ],
        namespace='transcripts')),
    url(r'^paying-for-college/',
        include_if_app_enabled('comparisontool', 'comparisontool.urls')),
    url(r'^paying-for-college2/',
        include_if_app_enabled(
            'paying_for_college', 'paying_for_college.config.urls')),
    url(r'^credit-cards/agreements/',
        include_if_app_enabled('agreements', 'agreements.urls')),
    url(r'^selfregs/',
        include_if_app_enabled('selfregistration', 'selfregistration.urls')),
    url(r'^hud-api-replace/', include_if_app_enabled(
        'hud_api_replace',
        'hud_api_replace.urls',
        namespace='hud_api_replace')),
    url(r'^retirement/',
        include_if_app_enabled('retirement_api', 'retirement_api.urls')),

    url(r'^data-research/consumer-complaints/',
        include_if_app_enabled('complaintdatabase', 'complaintdatabase.urls')),

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

    flagged_url('EREGS20',
                r'^eregs2/',
                include_if_app_enabled('eregs_core', 'eregs_core.urls')
                ),
    url(r'^eregs-api/',
        include_if_app_enabled('regcore', 'regcore.urls')),
    url(r'^eregulations/',
        include_if_app_enabled('regulations', 'regulations.urls')),

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
    url(r'^token-provider/', token_provider),

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
    url(r'^(?P<language>es)/obtener-respuestas/buscar/?$',
        ask_search,
        name='ask-search-es'),
    url(r'^(?P<language>es)/obtener-respuestas/buscar/(?P<as_json>json)/$',
        ask_search,
        name='ask-search-es-json'),
    url(r'^(?i)ask-cfpb/([-\w]{1,244})-(en)-(\d{1,6})/?$',
        view_answer,
        name='ask-english-answer'),
    url(r'^es/obtener-respuestas/([-\w]{1,244})-(es)-(\d{1,6})/?$',
        view_answer,
        name='ask-spanish-answer'),
    url(r'^es/obtener-respuestas/([-\w]{1,244})-(es)-(\d{1,6})/imprimir/?$',
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

    es_conv_flag(r'^es/$', TemplateView.as_view(
                 template_name='/es/index.html')),

    es_conv_flag(r'^es/hogar/$', TemplateView.as_view(
                 template_name='es/hogar/index.html')),

    es_conv_flag(r'^es/nuestra-historia/$', TemplateView.as_view(
                 template_name='es/nuestra-historia/index.html')),

    es_conv_flag(r'^es/presentar-una-queja/$', TemplateView.as_view(
                 template_name='es/presentar-una-queja/index.html')),

    es_conv_flag(r'^es/quienes-somos/$', TemplateView.as_view(
                 template_name='es/quienes-somos/index.html')),

    url(r'^_status/', include_if_app_enabled('watchman', 'watchman.urls')),

    flagged_url('FWB_RELEASE',
                r'^(?i)consumer-tools/financial-well-being/',
                include('wellbeing.urls')
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
        url(r'^picard/(?P<path>.*)$',
            RedirectView.as_view(url='/admin/cdn/%(path)s', permanent=True)),

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
            'django.contrib.auth.views.password_change',
            {'password_change_form': CFGOVPasswordChangeForm}),
        url(r'^password/change/done/$',
            auth_views.password_change_done,
            name='password_change_done'),
        url(r'^admin/account/change_password/$',
            change_password,
            name='wagtailadmin_account_change_password'),
        url(r'^django-admin/', include(admin.site.urls)),
        url(r'^admin/', include(wagtailadmin_urls)),

    ]

    if 'selfregistration' in settings.INSTALLED_APPS:
        patterns.append(url(r'^selfregs/', include('selfregistration.urls')))

    if 'csp.middleware.CSPMiddleware' in settings.MIDDLEWARE_CLASSES:
        # allow browsers to push CSP error reports back to the server
        patterns.append(url(r'^csp-report/',
                            'core.views.csp_violation_report'))

    urlpatterns = patterns + urlpatterns


if 'selfregistration' in settings.INSTALLED_APPS:
    from selfregistration.views import CompanySignup
    pattern = url(r'^company-signup/', CompanySignup.as_view())
    urlpatterns.append(pattern)

if settings.DEBUG:
    urlpatterns.append(
        url(r'^test-fixture/$',
            SheerTemplateView.as_view(
                template_name='test-fixture/index.html'),
            name='test-fixture')
    )
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
