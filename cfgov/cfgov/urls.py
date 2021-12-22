from functools import partial

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView, TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtailsharing import urls as wagtailsharing_urls
from wagtailsharing.views import ServeView

from flags.urls import flagged_re_path
from flags.views import FlaggedTemplateView
from wagtailautocomplete.urls.admin import (
    urlpatterns as autocomplete_admin_urls
)

from ask_cfpb.views import (
    ask_autocomplete, ask_search, redirect_ask_search, view_answer
)
from core.decorators import akamai_no_store
from core.views import (
    ExternalURLNoticeView, govdelivery_subscribe, regsgov_comment
)
from housing_counselor.views import (
    HousingCounselorPDFView, HousingCounselorView
)
from legacy.views.complaint import CCDBSearchView, ComplaintLandingView
from regulations3k.views import redirect_eregs
from v1.auth_forms import CFGOVPasswordChangeForm
from v1.views import (
    change_password, check_permissions, login_with_lockout,
    password_reset_confirm
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
    """If flag is set, serve page from Wagtail, otherwise raise 404."""
    def this_view_always_raises_http404(request, *args, **kwargs):
        raise Http404('flag {} not set'.format(flag_name))

    return flagged_re_path(
        flag_name,
        regex_path,
        lambda request: ServeView.as_view()(request, request.path),
        fallback=this_view_always_raises_http404,
        name=url_name,
    )


def empty_200_response(request, *args, **kwargs):
    return HttpResponse(status=200)


urlpatterns = [

    re_path(r'^rural-or-underserved-tool/$', TemplateView.as_view(
        template_name='rural-or-underserved/index.html'),
        name='rural-or-underserved'),

    re_path(
        r'^documents/(?P<document_id>\d+)/(?P<document_filename>.*)$',
        DocumentServeView.as_view(),
        name='wagtaildocs_serve'
    ),

    re_path(
        r'^home/(?P<path>.*)$',
        RedirectView.as_view(url='/%(path)s', permanent=True)
    ),

    re_path(r'^owning-a-home/static/(?P<path>.*)$', RedirectView.as_view(
        url='/static/owning-a-home/static/%(path)s', permanent=True)),
    re_path(r'^owning-a-home/resources/(?P<path>.*)$', RedirectView.as_view(
        url='/static/owning-a-home/resources/%(path)s',
        permanent=True)),
    re_path(r'^owning-a-home/closing-disclosure/$', TemplateView.as_view(
        template_name='owning-a-home/closing-disclosure/index.html'),
        name='closing-disclosure'
    ),
    re_path(r'^owning-a-home/explore-rates/', TemplateView.as_view(
        template_name='owning-a-home/explore-rates/index.html'),
        name='explore-rates'
    ),
    re_path(r'^owning-a-home/loan-estimate/$', TemplateView.as_view(
        template_name='owning-a-home/loan-estimate/index.html'),
        name='loan-estimate'
    ),

    # Temporarily serve Wagtail OAH journey pages at `/process/` urls.
    # TODO: change to redirects after 2018 homebuying campaign.
    re_path(
        r'^owning-a-home/process/(?P<path>.*)$',
        lambda req, path: ServeView.as_view()(
            req, 'owning-a-home/{}'.format(path or 'prepare/')
        ),
    ),
    # END TODO

    re_path(
        r'^know-before-you-owe/$',
        TemplateView.as_view(
            template_name='know-before-you-owe/index.html'),
        name='know-before-you-owe'
    ),
    re_path(
        r'^know-before-you-owe/timeline/$',
        TemplateView.as_view(
            template_name='know-before-you-owe/timeline/index.html'),
        name='kbyo-timeline'
    ),
    re_path(
        r'^know-before-you-owe/compare/$',
        TemplateView.as_view(
            template_name='know-before-you-owe/compare/index.html'),
        name='kbyo-compare'
    ),

    re_path(r'^your-story/$', TemplateView.as_view(
        template_name='/your-story/index.html')),

    re_path(r'^parents/(?P<path>.*)$', RedirectView.as_view(
        url='/money-as-you-grow/%(path)s', permanent=True)),
    re_path(r'^blog/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/blog/%(path)s', permanent=True)),
    re_path(r'^newsroom/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/newsroom/%(path)s', permanent=True)),

    re_path(r'^the-bureau/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/the-bureau/%(path)s', permanent=True)),

    re_path(
        r'^about-us/leadership-calendar/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/the-bureau/leadership-calendar/%(path)s',
            permanent=True)
    ),

    re_path(
        r'^doing-business-with-us/(?P<path>.*)$',
        RedirectView.as_view(
            url='/about-us/doing-business-with-us/%(path)s', permanent=True)
    ),

    re_path(
        r'^external-site/$', ExternalURLNoticeView.as_view(),
        name='external-site'
    ),

    re_path(
        r'^subscriptions/new/$', govdelivery_subscribe,
        name='govdelivery'
    ),

    re_path(
        r'^govdelivery-subscribe/', include((
            [
                re_path(
                    r'^success/$',
                    TemplateView.as_view(
                        template_name='govdelivery-subscribe/success/index.html'  # noqa: E501
                    ),
                    name='success'
                ),
                re_path(
                    r'^error/$',
                    TemplateView.as_view(
                        template_name='govdelivery-subscribe/error/index.html'
                    ),
                    name='user_error'
                ),
                re_path(
                    r'^server-error/$',
                    TemplateView.as_view(
                        template_name='govdelivery-subscribe/server-error/index.html'  # noqa: E501
                    ),
                    name='server_error'
                )
            ],
            'govdelivery'),
            namespace='govdelivery')
    ),

    re_path(r'^regulation-comment/new/$', regsgov_comment, name='reg_comment'),

    re_path(r'^regulation-comment/', include((
        [
            re_path(r'^success/$', TemplateView.as_view(
                template_name='regulation-comment/success/index.html'),
                # 'core.views.comment_success',
                name='success'),
            re_path(r'^error/$', TemplateView.as_view(
                template_name='regulation-comment/error/index.html'),
                name='user_error'),
            re_path(r'^server-error/$', TemplateView.as_view(
                template_name='regulation-comment/server-error/index.html'),
                name='server_error')
        ],
        'reg_comment'),
        namespace='reg_comment')),

    re_path(r'^feed/$', RedirectView.as_view(
        url='/about-us/blog/feed/', permanent=True)),
    re_path(r'^feed/blog/$', RedirectView.as_view(
        url='/about-us/blog/feed/', permanent=True)),
    re_path(r'^feed/newsroom/$', RedirectView.as_view(
        url='/about-us/newsroom/feed/', permanent=True)),
    re_path(r'^newsroom-feed/$', RedirectView.as_view(
        url='/about-us/newsroom/feed/', permanent=True)),

    re_path(r'^careers/(?P<path>.*)$', RedirectView.as_view(
        url='/about-us/careers/%(path)s', permanent=True)),

    re_path(r'^transcripts/', include((
        [
            re_path(
                r'^how-to-apply-for-a-federal-job-with-the-cfpb/$',
                TemplateView.as_view(
                    template_name='transcripts/how-to-apply-for-a-federal-job-with-the-cfpb/index.html'),  # noqa: E501
                name='how-to-apply-for-a-federal-job-with-the-cfpb'
            ),
        ],
        'transcripts'),
        namespace='transcripts')),

    re_path(
        r'^paying-for-college/repay-student-debt/$',
        TemplateView.as_view(
            template_name='paying-for-college/repay_student_debt.html'
        ),
        name='pfc-repay'
    ),

    re_path(
        r'^paying-for-college2/',
        include(
            ('paying_for_college.urls', 'paying_for_college'),
            namespace='paying_for_college'
        )
    ),

    re_path(r'^credit-cards/agreements/', include('agreements.urls')),

    re_path(
        r'^data-research/prepaid-accounts/search-agreements/',
        include((
            'prepaid_agreements.urls',
            'prepaid_agreements'),
            namespace='prepaid_agreements')),

    re_path(
        r'^consumer-tools/retirement/',
        include('retirement_api.urls', namespace='retirement_api')
    ),

    re_path(
        r'^data-research/consumer-complaints/$',
        ComplaintLandingView.as_view(),
        name='complaint-landing'
    ),

    # CCDB5-API
    re_path(
        r'^data-research/consumer-complaints/search/api/v1/',
        include('complaint_search.urls')
    ),
    # CCDB5-UI
    re_path(
        r'^data-research/consumer-complaints/search/',
        CCDBSearchView.as_view(),
        name='complaint-search'
    ),

    re_path(r'^oah-api/rates/', include('ratechecker.urls')),
    re_path(r'^oah-api/county/', include('countylimits.urls')),

    re_path(
        r'^find-a-housing-counselor/$',
        HousingCounselorView.as_view(),
        name='housing-counselor'
    ),
    re_path(
        r'^save-hud-counselors-list/$',
        HousingCounselorPDFView.as_view(),
        name='housing-counselor-pdf'
    ),

    # Report redirects
    re_path(r'^reports/(?P<path>.*)$', RedirectView.as_view(
        url='/data-research/research-reports/%(path)s',
        permanent=True)),

    # data-research-api
    re_path(
        r'^data-research/mortgages/api/v1/',
        include('data_research.urls')
    ),

    # educational resources
    re_path(
        r'^consumer-tools/educator-tools/resources-youth-employment-programs/transportation-tool/$',  # noqa: E501
        TemplateView.as_view(
            template_name='youth_employment_success/index.html'
        ),
        name='youth_employment_success'
    ),

    # retirement redirects
    re_path(r'^retirement/(?P<path>.*)$', RedirectView.as_view(
            url='/consumer-tools/retirement/%(path)s',
            permanent=True)),

    # empowerment redirects
    re_path(r'^empowerment/$', RedirectView.as_view(
            url='/consumer-tools/educator-tools/economically-vulnerable/',
            permanent=True)),

    # students redirects
    re_path(r'^students/(?P<path>.*)$', RedirectView.as_view(
            url='/consumer-tools/educator-tools/students/%(path)s',
            permanent=True)),

    # ask-cfpb
    re_path(
        r'^askcfpb/$',
        RedirectView.as_view(url='/ask-cfpb/', permanent=True)
    ),
    re_path(
        r'^(?P<language>es)/obtener-respuestas/c/(.+)/(?P<ask_id>\d+)/(.+)\.html$',  # noqa: E501
        RedirectView.as_view(
            url='/es/obtener-respuestas/slug-es-%(ask_id)s',
            permanent=True
        )
    ),
    re_path(
        r'^askcfpb/(?P<ask_id>\d+)/(.*)$',
        RedirectView.as_view(
            url='/ask-cfpb/slug-en-%(ask_id)s',
            permanent=True)),
    re_path(
        r'^askcfpb/search/',
        redirect_ask_search,
        name='redirect-ask-search'
    ),
    re_path(
        r'^ask-cfpb/([-\w]{1,244})-(en)-(\d{1,6})/$',
        view_answer,
        name='ask-english-answer'
    ),
    re_path(
        r'^es/obtener-respuestas/([-\w]{1,244})-(es)-(\d{1,6})/$',
        view_answer,
        name='ask-spanish-answer'
    ),
    re_path(
        r'^es/obtener-respuestas/([-\w]{1,244})-(es)-(\d{1,6})/imprimir/$',
        view_answer,
        name='ask-spanish-answer'
    ),

    re_path(
        r'^(?P<language>es)/obtener-respuestas/buscar/$',
        ask_search,
        name='ask-search-es'
    ),
    re_path(
        r'^(?P<language>es)/obtener-respuestas/buscar/(?P<as_json>json)/$',
        ask_search,
        name='ask-search-es-json'
    ),
    re_path(
        r'^ask-cfpb/search/$',
        ask_search,
        name='ask-search-en'
    ),
    re_path(
        r'^ask-cfpb/search/(?P<as_json>json)/$',
        ask_search,
        name='ask-search-en-json'
    ),
    re_path(
        r'^ask-cfpb/api/autocomplete/$',
        ask_autocomplete,
        name='ask-autocomplete-en'
    ),
    re_path(
        r'^(?P<language>es)/obtener-respuestas/api/autocomplete/$',
        ask_autocomplete,
        name='ask-autocomplete-es'
    ),

    re_path(
        r'^consumer-tools/financial-well-being/',
        include('wellbeing.urls')
    ),
    re_path(
        r'^about-us/diversity-and-inclusion/',
        include((
            'diversity_inclusion.urls',
            'diversity_inclusion'),
            namespace='diversity_inclusion')),

    re_path(
        r'^privacy/',
        include((
            'privacy.urls',
            'privacy'),
            namespace='privacy')),

    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
    )),
    re_path(r'^sitemap\.xml$', akamai_no_store(sitemap), name='sitemap'),

    re_path(
        r'^consumer-tools/educator-tools/youth-financial-education/',
        include('teachers_digital_platform.urls')
    ),

    re_path(
        r'^consumer-tools/educator-tools/youth-financial-education/curriculum-review/',  # noqa: E501
        include('crtool.urls')
    ),

    re_path(
        r'^regulations3k-service-worker.js',
        TemplateView.as_view(
            template_name='regulations3k/regulations3k-service-worker.js',
            content_type='application/javascript'
        ),
        name='regulations3k-service-worker.js'
    ),

    # Explicitly redirect eRegulations URLs to Regulations3000
    re_path(r'^eregulations/.*', redirect_eregs, name='eregs-redirect'),

    # Manually enabled when Beta is being used for an external test.
    # Jenkins job check this endpoint to determine whether to refresh
    # Beta database.
    flagged_re_path(
        'BETA_EXTERNAL_TESTING',
        r'^beta_external_testing/',
        akamai_no_store(empty_200_response)
    ),
]

# Ask CFPB category and subcategory redirects
category_redirects = [
    re_path(
        r'^ask-cfpb/category-auto-loans/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/auto-loans/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-bank-accounts-and-services/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/bank-accounts/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-credit-cards/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/credit-cards/answers/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-credit-reporting/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/credit-reports-and-scores/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-debt-collection/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/debt-collection/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-families-money/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/money-as-you-grow/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-money-transfers/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/money-transfers/answers/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-mortgages/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/mortgages/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-payday-loans/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/payday-loans/answers',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-prepaid-cards/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/prepaid-cards/',
            permanent=True)
    ),
    re_path(
        r'^ask-cfpb/category-student-loans/(.*)$',
        RedirectView.as_view(
            url='/consumer-tools/student-loans/',
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-comprar-un-vehiculo/(.*)$',
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/prestamos-para-vehiculos/respuestas/',  # noqa: E501
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-manejar-una-cuenta-bancaria/(.*)$',  # noqa: E501
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/cuentas-bancarias/',
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-obtener-una-tarjeta-de-credito/(.*)$',  # noqa: E501
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/tarjetas-de-credito/respuestas/',  # noqa: E501
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-adquirir-credito/(.*)$',
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/informes-y-puntajes-de-credito/',  # noqa: E501
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-manejar-una-deuda/(.*)$',
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/cobro-de-deudas/',
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-ensenar-a-otros/(.*)$',
        RedirectView.as_view(
            url='/es/el-dinero-mientras-creces/',
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-enviar-dinero/(.*)$',
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/transferencias-de-dinero/respuestas/',  # noqa: E501
            permanent=True)
    ),
    re_path(r'^es/obtener-respuestas/categoria-comprar-una-casa/(.*)$',
            RedirectView.as_view(
                url='/es/herramientas-del-consumidor/hipotecas/',
                permanent=True)),
    re_path(
        r'^es/obtener-respuestas/categoria-prestamos-de-dia-de-pago/(.*)$',
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/prestamos-del-dia-de-pago/',  # noqa: E501
            permanent=True)
    ),
    re_path(
        r'^es/obtener-respuestas/categoria-escoger-una-tarjeta-prepagada/(.*)$',  # noqa: E501
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/tarjetas-prepagadas/respuestas/',  # noqa: E501
            permanent=True)),
    re_path(
        r'^es/obtener-respuestas/categoria-pagar-la-universidad/(.*)$',
        RedirectView.as_view(
            url='/es/herramientas-del-consumidor/prestamos-estudiantiles/',  # noqa: E501
            permanent=True)
    )
]
urlpatterns = urlpatterns + category_redirects

if settings.ALLOW_ADMIN_URL:
    patterns = [
        re_path(r'^login/$', login_with_lockout, name='cfpb_login'),
        re_path(
            r'^login/check_permissions/$',
            check_permissions,
            name='check_permissions'
        ),
        re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
        re_path(
            r'^admin/login/$',
            RedirectView.as_view(
                url='/login/',
                permanent=True,
                query_string=True
            )
        ),
        re_path(
            r'^django-admin/login/$',
            RedirectView.as_view(
                url='/login/',
                permanent=True,
                query_string=True
            )
        ),

        re_path(
            r'^django-admin/password_change',
            change_password,
            name='django_admin_account_change_password'
        ),
        re_path(r'^django-admin/', admin.site.urls),

        # Override Django and Wagtail password views with our password policy
        re_path(r'^admin/password_reset/', include([
            re_path(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa: E501
                password_reset_confirm,
                name='password_reset_confirm')
        ])),
        re_path(
            r'^django-admin/password_change',
            auth_views.PasswordChangeView.as_view(),
            {'password_change_form': CFGOVPasswordChangeForm}
        ),
        re_path(
            r'^password/change/done/$',
            auth_views.PasswordChangeDoneView.as_view(),
            name='password_change_done'
        ),
        re_path(
            r'^admin/account/change_password/$',
            change_password,
            name='wagtailadmin_account_change_password'
        ),
        re_path(r'^admin/autocomplete/', include(autocomplete_admin_urls)),
        re_path(r'^admin/', include(wagtailadmin_urls)),

    ]

    urlpatterns = patterns + urlpatterns

if settings.WATCHMAN_TOKENS is not None:
    urlpatterns.append(
        re_path(r'^_status/', include('watchman.urls')),
    )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # enable local preview of error pages
    urlpatterns.append(
        re_path(r'^500/$', TemplateView.as_view(template_name='500.html'),
                name='500'))
    urlpatterns.append(
        re_path(r'^404/$', TemplateView.as_view(template_name='404.html'),
                name='404'))

    try:
        import debug_toolbar
        urlpatterns.append(re_path(r'^__debug__/',
                                   include(debug_toolbar.urls)))
    except ImportError:
        pass

# Catch remaining URL patterns that did not match a route thus far.
urlpatterns.append(re_path(r'', include(wagtailsharing_urls)))


def handle_error(code, request, exception=None):
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
