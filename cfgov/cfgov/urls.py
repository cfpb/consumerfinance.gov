import os

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.views.generic.base import TemplateView, RedirectView
from legacy.views import HousingCounselorPDFView, dbrouter_shortcut, token_provider
from sheerlike.views.generic import SheerTemplateView
from sheerlike.sites import SheerSite

from v1.views import LeadershipCalendarPDFView, unshare, change_password, \
                     password_reset_confirm, login_with_lockout,\
                     check_permissions, welcome
from v1.auth_forms import CFGOVPasswordChangeForm

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from transition_utilities.conditional_urls import include_if_app_enabled

fin_ed = SheerSite('fin-ed-resources')

urlpatterns = [

    url(r'^documents/', include(wagtaildocs_urls)),
    # TODO: Enable search route when search is available.
    # url(r'^search/$', 'search.views.search', name='search'),

    url(r'^home/(?P<path>.*)$', RedirectView.as_view(url='/%(path)s', permanent=True)),

    url(r'^owning-a-home/static/(?P<path>.*)$', RedirectView.as_view(url='/static/owning-a-home/static/%(path)s')),
    url(r'^owning-a-home/resources/(?P<path>.*)$', RedirectView.as_view(url='/static/owning-a-home/resources/%(path)s')),
    url(r'^owning-a-home/', include(SheerSite('owning-a-home').urls)),

    # the two redirects are an unfortunate workaround, could be resolved by
    # using static('path/to/asset') in the source template

    url(r'^tax-time-saving/static/(?P<path>.*)$', RedirectView.as_view(url='/static/tax-time-saving/static/%(path)s')),
    url(r'^tax-time-saving/', include(SheerSite('tax-time-saving').urls)),
    url(r'^know-before-you-owe/static/(?P<path>.*)$', RedirectView.as_view(url='/static/know-before-you-owe/static/%(path)s')),
    url(r'^know-before-you-owe/', include(SheerSite('know-before-you-owe').urls)),

    url(r'^adult-financial-education/', include(fin_ed.urls_for_prefix('adult-financial-education'))),
    url(r'^youth-financial-education/', include(fin_ed.urls_for_prefix('youth-financial-education'))),
    url(r'^library-resources/', include(fin_ed.urls_for_prefix('library-resources'))),
    url(r'^tax-preparer-resources/', include(fin_ed.urls_for_prefix('tax-preparer-resources'))),
    url(r'^managing-someone-elses-money/', include(fin_ed.urls_for_prefix('managing-someone-elses-money'))),
    url(r'^parents/(?P<path>.*)$', RedirectView.as_view(url='/money-as-you-grow/%(path)s', permanent=True)),
    url(r'^money-as-you-grow/', include(fin_ed.urls_for_prefix('money-as-you-grow'))),
    url(r'fin-ed/privacy-act-statement/', include(fin_ed.urls_for_prefix('privacy-act-statement'))),
    url(r'^docs/', include([
        url(r'^$', SheerTemplateView.as_view(template_name='docs_index.html'), name='index'),

        url(r'^sheer-layouts/', include([
            url(r'^$', SheerTemplateView.as_view(template_name='sheer-layouts/index.html'), name='index'),
            url(r'^jinja-content-blocks/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/jinja-content-blocks/index.html'),
                name='jinja-content-blocks'),
            url(r'^content-base/$', SheerTemplateView.as_view(template_name='sheer-layouts/content-base/index.html'),
                name='content-base'),
            url(r'^content-base-main-first/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/content-base-main-first/index.html'),
                name='content-base-main-first'),
            url(r'^content-base-sidebar-first/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/content-base-sidebar-first/index.html'),
                name='content-base-sidebar-first'),
            url(r'^layout-1-3/$', SheerTemplateView.as_view(template_name='sheer-layouts/layout-1-3/index.html'),
                name='layout-1-3'),
            url(r'^layout-side-nav/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/layout-side-nav/index.html'),
                name='layout-side-nav'),
            url(r'^layout-2-1/$', SheerTemplateView.as_view(template_name='sheer-layouts/layout-2-1/index.html'),
                name='layout-2-1'),
            url(r'^layout-2-1-bleedbar/$',
                SheerTemplateView.as_view(template_name='sheer-layouts/layout-2-1-bleedbar/index.html'),
                name='layout-2-1-bleedbar'),
            url(r'^hero/$', SheerTemplateView.as_view(template_name='sheer-layouts/hero/index.html'),
                name='hero'),
        ],
            namespace='sheer-layouts')),


        url(r'^blog-docs/$', SheerTemplateView.as_view(template_name='blog-docs/index.html'), name='blog-docs'),
        url(r'^cf-enhancements/$', SheerTemplateView.as_view(template_name='cf-enhancements/index.html'),
            name='cf-enhancements'),
        url(r'^forms/$', SheerTemplateView.as_view(template_name='forms/index.html'), name='doc-forms'),
        url(r'^header/$', SheerTemplateView.as_view(template_name='header/index.html'), name='doc-header'),
        url(r'^lists/$', SheerTemplateView.as_view(template_name='lists/index.html'), name='doc-lists'),
        url(r'^media/$', SheerTemplateView.as_view(template_name='media/index.html'), name='doc-media'),
        url(r'^media-object/$', SheerTemplateView.as_view(template_name='media/index.html'), name='doc-media-object'),
        url(r'^meta/$', SheerTemplateView.as_view(template_name='meta/index.html'), name='doc-meta'),
        url(r'^misc/$', SheerTemplateView.as_view(template_name='misc/index.html'), name='doc-misc'),
        url(r'^nav-secondary/$', SheerTemplateView.as_view(template_name='nav-secondary/index.html'),
            name='nav-secondary'),
        url(r'^post/$', SheerTemplateView.as_view(template_name='post/index.html'), name='doc-post'),
        url(r'^print/$', SheerTemplateView.as_view(template_name='print/index.html'), name='doc-print'),
        url(r'^summary/$', SheerTemplateView.as_view(template_name='summary/index.html'), name='doc-summary'),

    ],
        namespace='docs')),


    url(r'^blog/(?P<path>.*)$', RedirectView.as_view(url='/about-us/blog/%(path)s', permanent=True)),
    url(r'^newsroom/(?P<path>.*)$', RedirectView.as_view(url='/about-us/newsroom/%(path)s', permanent=True)),

    url(r'^about-us/newsroom/press-resources/$',
        TemplateView.as_view(
            template_name='newsroom/press-resources/index.html'),
            name='press-resources'),

    url(r'^the-bureau/(?P<path>.*)$', RedirectView.as_view(url='/about-us/the-bureau/%(path)s', permanent=True)),
    url(r'^about-us/the-bureau/', include([
        url(r'^$', SheerTemplateView.as_view(template_name='about-us/the-bureau/index.html'),
            name='index'),
        url(r'^leadership-calendar/$',
            SheerTemplateView.as_view(),
            name='leadership-calendar'),
        url(r'^(?P<page_slug>[\w-]+)/$',
            SheerTemplateView.as_view(),
            name='page'),
        url(r'^leadership-calendar/pdf/$',
            LeadershipCalendarPDFView.as_view(),
            name='leadership-calendar-pdf'),
        url(r'^leadership-calendar/print/$',
            SheerTemplateView.as_view(template_name='about-us/the-bureau/leadership-calendar/print/index.html'),
            name='leadership-calendar-print')],
        namespace='the-bureau')),


    url(r'^doing-business-with-us/(?P<path>.*)$', RedirectView.as_view(url='/about-us/doing-business-with-us/%(path)s', permanent=True)),
    url(r'^about-us/doing-business-with-us/', include([
        url(r'^$',
            TemplateView.as_view(template_name='about-us/doing-business-with-us/index.html'),
            name='index'),
        url(r'^(?P<page_slug>[\w-]+)/$',
            SheerTemplateView.as_view(),
            name='page')],
        namespace='business')),

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
            #'core.views.comment_success',
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

    url(r'^feed/$', RedirectView.as_view(url='/about-us/blog/feed/')),
    url(r'^feed/blog/$', RedirectView.as_view(url='/about-us/blog/feed/')),
    url(r'^feed/newsroom/$', RedirectView.as_view(url='/about-us/newsroom/feed/')),
    url(r'^newsroom-feed/$', RedirectView.as_view(url='/about-us/newsroom/feed/')),

    url(r'^about-us/$', SheerTemplateView.as_view(template_name='about-us/index.html'), name='about-us'),

    url(r'^external-site/$', SheerTemplateView.as_view(template_name='external-site/index.html'), name='external-site'),

    url(r'^careers/(?P<path>.*)$', RedirectView.as_view(url='/about-us/careers/%(path)s', permanent=True)),
    url(r'^about-us/careers/', include('jobmanager.urls', namespace='careers')),

    url(r'^transcripts/', include([
        url(r'^how-to-apply-for-a-federal-job-with-the-cfpb/$', SheerTemplateView.as_view(
            template_name='transcripts/how-to-apply-for-a-federal-job-with-the-cfpb/index.html'),
            name='how-to-apply-for-a-federal-job-with-the-cfpb'),
    ],
        namespace='transcripts')),
    url(r'^paying-for-college/', include_if_app_enabled('comparisontool','comparisontool.urls')),
    url(r'^paying-for-college2/', include_if_app_enabled('paying_for_college','paying_for_college.config.urls')),
    url(r'^credit-cards/agreements/', include_if_app_enabled('agreements','agreements.urls')),
    url(r'^(?i)askcfpb/', include_if_app_enabled('knowledgebase','knowledgebase.urls')),
    url(r'^es/obtener-respuestas/', include_if_app_enabled('knowledgebase','knowledgebase.babel_urls')),
    url(r'^selfregs/', include_if_app_enabled('selfregistration', 'selfregistration.urls')),
    url(r'^hud-api-replace/', include_if_app_enabled('hud_api_replace','hud_api_replace.urls')),
    url(r'^retirement/', include_if_app_enabled('retirement_api','retirement_api.urls')),
    url(r'^complaint/', include_if_app_enabled('complaint','complaint.urls')),
    url(r'^data-research/consumer-complaints/', include_if_app_enabled('complaintdatabase','complaintdatabase.urls')),
    url(r'^oah-api/rates/', include_if_app_enabled('ratechecker', 'ratechecker.urls')),
    url(r'^oah-api/county/', include_if_app_enabled('countylimits','countylimits.urls')),
    url(r'^eregs-api/', include_if_app_enabled('regcore', 'regcore.urls')),
    url(r'^eregulations/', include_if_app_enabled('regulations','regulations.urls')),

    url(r'^find-a-housing-counselor/$', TemplateView.as_view(template_name='find_a_housing_counselor.html')),
    url(r'^save-hud-counselors-list/$', HousingCounselorPDFView.as_view()),
    # Report redirects
    url(r'^reports/(?P<path>.*)$', RedirectView.as_view(url='/data-research/research-reports/%(path)s', permanent=True)),
    url(r'^jobs/supervision/$', TemplateView.as_view(template_name='jobmanager/supervision.html'), name='jobs_supervision'),

    url(r'^jobs/technology-innovation-fellows/$',
        TemplateView.as_view(template_name='jobmanager/technology-innovation-fellows.html'),
        name='technology_innovation_fellows'),
    url(r'^jobs/fellowship_form_submit/$', 'jobmanager.views.fellowship_form_submit', name='fellowship_form_submit'),

    # Form crsf token provider for JS form submission
    url(r'^token-provider/', token_provider)
]

if settings.ALLOW_ADMIN_URL:
    patterns = [
        url(r'^login/$', login_with_lockout, name='cfpb_login'),
        url(r'^login/check_permissions/$', check_permissions, name='check_permissions'),
        url(r'^login/welcome/$', welcome, name='welcome'),
        url('admin/login/$', RedirectView.as_view(url='/login/', permanent=True, query_string=True)),
        url('django-admin/login/$', RedirectView.as_view(url='/login/', permanent=True, query_string=True)),

        url(r'^d/admin/(?P<path>.*)$', RedirectView.as_view(url='/django-admin/%(path)s',permanent=True)),
        url(r'^picard/(?P<path>.*)$', RedirectView.as_view(url='/tasks/%(path)s',permanent=True)),
        url(r'^django-admin/password_change', change_password, name='django_admin_account_change_password'),
        url(r'^django-admin/', include(admin.site.urls)),
        url(r'^admin/pages/(\d+)/unshare/$', unshare, name='unshare'),

        # - Override Django and Wagtail password views with our password policy - #
        url(r'^admin/password_reset/', include([
            url(
                r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                password_reset_confirm, name='password_reset_confirm',
            )
        ])),
        url(r'^django-admin/password_change', 'django.contrib.auth.views.password_change',
            {'password_change_form': CFGOVPasswordChangeForm}),
        url(r'^password/change/done/$',
            auth_views.password_change_done,
            name='password_change_done'),
        url(r'^admin/account/change_password/$', change_password, name='wagtailadmin_account_change_password'),
        url(r'^django-admin/', include(admin.site.urls)),
        url(r'^admin/', include(wagtailadmin_urls)),
        url(r'^admin/pages/(\d+)/unshare/$', unshare, name='unshare'),

    ]

    if os.environ.get('DATABASE_ROUTING', False):
        patterns = [url(r'^django-admin/r/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$', dbrouter_shortcut)] + patterns

    if 'picard' in settings.INSTALLED_APPS:
        patterns.append(url(r'^tasks/', include('picard.urls')))

    if 'selfregistration' in settings.INSTALLED_APPS:
        patterns.append(url(r'^selfregs/', include('selfregistration.urls')))

    urlpatterns = patterns + urlpatterns

if 'cfpb_common' in settings.INSTALLED_APPS:
    patterns= [url(r'^token-provider/', 'cfpb_common.views.token_provider'),
               url(r'^credit-cards/knowbeforeyouowe/$', TemplateView.as_view(template_name='knowbeforeyouowe/creditcards/tool.html'), name='cckbyo'),
               ]
    urlpatterns += patterns

if 'cal' in settings.INSTALLED_APPS:
    from cal.views import CalendarJSONList
    patterns= [url(r'^leadership-calendar/cfpb-leadership.json$', CalendarJSONList.as_view()),
               ]
    urlpatterns += patterns

if 'selfregistration' in settings.INSTALLED_APPS:
    from selfregistration.views import CompanySignup
    pattern = url(r'^company-signup/', CompanySignup.as_view())
    urlpatterns.append(pattern)

if settings.DEBUG :
    urlpatterns.append(url(r'^test-fixture/$', SheerTemplateView.as_view(template_name='test-fixture/index.html'), name='test-fixture'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch remaining URL patterns that did not match a route thus far.

urlpatterns.append(url(r'', include(wagtail_urls)))

from sheerlike import register_permalink

register_permalink('posts', 'blog:detail')
register_permalink('newsroom', 'newsroom:detail')
register_permalink('office', 'offices:detail')
register_permalink('sub_page', 'sub_page:detail')
register_permalink('career', 'careers:career')
